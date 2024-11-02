from .models import Notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import NotificationSerializer
from .task import gather_infos


# Create your views here.
class Notifications(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(
            notifications,
            many=True,
        )
        return Response(serializer.data)


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
