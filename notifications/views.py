from .models import Notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status
from .serializers import NotificationSerializer
from django.db import transaction

from pywebpush import webpush
from django.conf import settings

import json
import logging

from .serviceChroma import chroma_service_notice

# from .task import gather_infos => for celery

# for webhook
logger = logging.getLogger("django")


# for webpush
def send_push(subscription, noti):
    message = json.dumps(
        {
            "code": noti.code,
            "tag": noti.tag,
            "title": noti.title,
            "writer": noti.writer,
            "etc": noti.etc,
        }
    )

    webpush(
        subscription_info=subscription,
        data=message,
        vapid_private_key=settings.VAPID_PRIVATE_KEY,
        vapid_claims={"sub": "mailto:yoosunu010@naver.com"},
    )


def create_multiple_notifications(notifications):

    try:
        # save multiple notis.
        noti_objs = [Notification(**notification) for notification in notifications]
        created_objs = Notification.objects.bulk_create(noti_objs)
        logger.info(f"✅ DB 저장 완료 ({len(created_objs)}개)")

        # ChromaDB Bulk Upsert
        try:
            ids = [str(obj.id) for obj in created_objs]
            documents = [
                f"{obj.title}\n{getattr(obj, 'content', '')[:500]}"
                for obj in created_objs
            ]

            metadatas = [
                {
                    "code": obj.code,
                    "tag": obj.tag,
                    "title": obj.title,
                    "link": obj.link,
                    "writer": obj.writer,
                    "etc": obj.etc,
                    "created_at": str(obj.created_at),
                }
                for obj in created_objs
            ]

            chroma_service_notice.collection.upsert(
                ids=ids, documents=documents, metadatas=metadatas
            )
        except Exception as e:
            print("❌ Chroma Bulk Upsert Error:", e)
            logger.error(f"❌ ChromaDB 동기화 에러: {e}", exc_info=True)

        # delete old things over 500
        notis = Notification.objects.order_by("-created_at")
        if notis.count() > 500:
            ids_to_delete = notis[500:].values_list("id", flat=True)
            Notification.objects.filter(id__in=ids_to_delete).delete()

        # delete old things over 500 (also delete chroma)
        notis = Notification.objects.order_by("-created_at")
        if notis.count() > 500:
            to_delete = notis[500:]
            ids_to_delete = list(to_delete.values_list("id", flat=True))

            # PostgreSQL delete
            Notification.objects.filter(id__in=ids_to_delete).delete()

            # ChromaDB delete
            try:
                chroma_service_notice.delete(ids=[str(pk) for pk in ids_to_delete])
            except Exception as e:
                print("❌ Chroma Bulk Delete Error:", e)
                logger.error(f"🚨 chroma delete error: {e}", exc_info=True)

        # webpush logic
        from subscriptions.models import Subs

        subscriptions = Subs.objects.all()

        for noti in noti_objs:
            for sub in subscriptions:
                subscription_info = {
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.keys_p256dh,
                        "auth": sub.keys_auth,
                    },
                }
                try:
                    send_push(subscription_info, noti)
                except Exception as e:
                    print("💥 Push Error:", e)

    except Exception as e:
        logger.error(f"🚨 알림 생성 프로세스 치명적 에러: {e}", exc_info=True)
        raise e


# Create your views here.
class Notifications(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return super().get_permissions()

    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(
            notifications,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        # print("wow: ", request.data) # for debug
        if not isinstance(data, list):
            data = [data]
        serializer = NotificationSerializer(
            data=data,
            many=True,
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # validated_data를 사용해 직접 bulk_create
                    create_multiple_notifications(serializer.validated_data)
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED,
                    )
            except Exception as e:
                logger = logging.getLogger("django")
                logger.error(
                    f"Notifications push error: {e}",
                    exc_info=True,
                )

                raise ParseError()
        else:
            # print(serializer.errors) for debug

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class NotificationDetail(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, code):
        try:
            notification = Notification.objects.get(code=code)
            return notification
        except Notification.DoesNotExist:
            raise NotFound

    def get(self, request, code):
        notification = self.get_object(code)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class NotificationSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q", "")

        # keyword base (PostgreSQL icontains)
        keyword_results = Notification.objects.filter(title__icontains=query)
        keyword_ids = list(keyword_results.values_list("id", flat=True))

        # vector base (ChromaDB)
        chroma_results = chroma_service_notice.search(query_text=query, result_limit=50)
        chroma_ids = [int(pk) for pk in chroma_results["ids"][0]]

        # combining (remove same case and maintain order)
        combined_ids = keyword_ids + [pk for pk in chroma_ids if pk not in keyword_ids]

        # results
        preserved_order = {pk: i for i, pk in enumerate(combined_ids)}
        final_queryset = Notification.objects.filter(id__in=combined_ids[:30])
        sorted_results = sorted(final_queryset, key=lambda x: preserved_order.get(x.id))

        serializer = NotificationSerializer(sorted_results, many=True)
        return Response(serializer.data)
