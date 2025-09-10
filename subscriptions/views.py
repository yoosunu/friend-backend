from django.shortcuts import render
from django.db import transaction
from .models import Subs
from .serializers import SubscriptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAdminUser

# debuging section
from django.http import JsonResponse
from django.core.management import call_command


# Create your views here.
class Subscription(APIView):

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    new_subscription = serializer.save(user=request.user)
                    serializer = SubscriptionSerializer(new_subscription)
                    return Response(serializer.data)
            except Exception:
                raise ParseError

        else:
            return Response(serializer.errors)


class SubscriptionsAdmin(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            subscriptions = Subs.objects.all()
            serializer = SubscriptionSerializer(
                subscriptions,
                many=True,
            )
            return Response(serializer.data)
        except Subs.DoesNotExist:
            raise NotFound

    # def delete(self, request)


# debuging section


# migrate logic
def force_migrate(request):
    try:
        call_command("makemigrations", interactive=False)
        call_command("migrate", interactive=False)
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"error": str(e)})


def debug_sub(request):
    data = []
    error_info = None
    try:
        for s in Subs.objects.all():
            data.append(
                {
                    "endpoint": s.endpoint or "No Endpoint",
                    "keys_p256dh": s.keys_p256dh or "",
                    "keys_auth": s.keys_auth or "",
                }
            )
    except Exception as e:
        # 에러 정보를 브라우저로 바로 보내기
        import traceback

        error_info = traceback.format_exc()
        return JsonResponse({"error": str(e), "traceback": error_info}, status=500)

    return JsonResponse(data, safe=False)
