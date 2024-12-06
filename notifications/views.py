from .models import Notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import NotificationSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .task import gather_infos


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class Notifications(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(
            notifications,
            many=True,
        )
        return Response(serializer.data)

    @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            new_notification = serializer.save()
            serializer = NotificationSerializer(new_notification)
            return Response(
                serializer.data,
                status=201,
            )
        else:
            print(serializer.errors)
            return Response(
                serializer.errors,
                status=400,
            )


class NotificationDetail(APIView):
    # permission_classes = [IsAdminUser]

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
