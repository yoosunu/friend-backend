from .models import Notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import NotificationSerializer
from django.db import transaction

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from .task import gather_infos


# Create your views here.
# @method_decorator(csrf_exempt, name="dispatch")
class Notifications(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(
            notifications,
            many=True,
        )
        return Response(serializer.data)

    # @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic:
                    new_notification = serializer.save()
                    serializer = NotificationSerializer(new_notification)
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED,
                    )
            except Exception:
                ParseError()
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class NotificationDetail(APIView):
    permission_classes = [IsAdminUser]

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
