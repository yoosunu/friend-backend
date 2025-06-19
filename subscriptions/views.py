from django.shortcuts import render
from django.db import transaction
from .models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from rest_framework.permissions import IsAdminUser


# Create your views here.
class Subscription(APIView):

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    new_subscription = serializer.save()
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
            subscriptions = Subscription.objects.all()
            serializer = SubscriptionSerializer(
                subscriptions,
                many=True,
            )
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            raise NotFound

    # def delete(self, request)
