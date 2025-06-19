from .models import Notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from .serializers import NotificationSerializer
from django.db import transaction

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from pywebpush import webpush
from django.conf import settings

import json

# from .task import gather_infos


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
        vapid_claims={
            "sub": "mailto:yoosunu010@naver.com",
        },
    )


def create_multiple_notifications(notifications):
    # save multiple notis.
    noti_objs = [Notification(**notification) for notification in notifications]
    Notification.objects.bulk_create(noti_objs)

    # webpush logic
    from subscriptions.models import Subscription

    subscriptions = Subscription.objects.all()

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

    # delete old things over 50
    notis = Notification.objects.order_by("-created_at")
    if notis.count() > 50:
        ids_to_delete = notis[50:].values_list("id", flat=True)
        Notification.objects.filter(id__in=ids_to_delete).delete()


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class Notifications(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(
            notifications,
            many=True,
        )
        return Response(serializer.data)

    # @method_decorator(csrf_exempt)
    # def post(self, request):
    #     serializer = NotificationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         try:
    #             with transaction.atomic():
    #                 new_notification = serializer.save()
    #                 serializer = NotificationSerializer(new_notification)
    #                 return Response(
    #                     serializer.data,
    #                     status=status.HTTP_201_CREATED,
    #                 )
    #         except Exception:
    #             raise ParseError()
    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    @method_decorator(csrf_exempt)
    def post(self, request):
        data = request.data
        if not isinstance(data, list):
            data = [data]
        serializer = NotificationSerializer(data=data, many=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # validated_data를 사용해 직접 bulk_create
                    create_multiple_notifications(serializer.validated_data)
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED,
                    )
            except Exception:
                raise ParseError()
        else:
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
