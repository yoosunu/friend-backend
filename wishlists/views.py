from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from items.models import Item


# Create your views here.
class wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishs = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            wishs,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            new_wish = serializer.save(
                user=request.user,
            )
            return Response(
                WishlistSerializer(new_wish).data,
            )
        else:
            return Response(serializer.errors)


class wishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            wish = Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound
        return wish

    def get(self, request, pk):
        wish = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wish,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        wish = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wish,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            updated_wish = serializer.save()
            return Response(WishlistSerializer(updated_wish).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        wish = self.get_object(pk, request.user)
        wish.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class wishlistItem(APIView):
    def get_wishs(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_item(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise NotFound

    def put(self, request, pk, item_pk):
        wish = self.get_wishs(pk=pk, user=request.user)
        item = self.get_item(pk=item_pk)
        if wish.items.filter(pk=item_pk).exists():
            wish.items.remove(item)
        else:
            wish.items.add(item)
        return Response(status=HTTP_200_OK)
