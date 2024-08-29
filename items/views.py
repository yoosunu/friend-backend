from django.conf import settings
from django.shortcuts import render
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .models import Item, Tag
from category.models import Category
from .serializers import (
    ItemListSerializer,
    ItemDetailSerializer,
    TagSerializer,
)
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer

# Create your views here.


class Items(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemListSerializer(
            items,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemListSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoice.chat:
                    raise ParseError("Wrong Category.")
            except Category.DoesNotExist:
                raise ParseError("Category Does Not exists.")

            try:
                with transaction.atomic():
                    new_item = serializer.save(
                        user=request.user,
                        category=category,
                    )
                    tags_pk = request.data.get("tags")
                    for tag_pk in tags_pk:
                        tag = Tag.objects.get(pk=tag_pk)
                        new_item.tags.add(tag)
                    serializer = ItemListSerializer(
                        new_item,
                        context={"request": request},
                    )
                    return Response(serializer.data)
            except Exception:
                ParseError("Tags not found.")

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ItemDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # a traditional way of getting the item.
    def get_object(self, pk):
        try:
            item = Item.objects.get(pk=pk)
            return item
        except Item.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = ItemDetailSerializer(
            self.get_object(pk),
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if item.user != request.user:
            raise PermissionDenied
        serializer = ItemDetailSerializer(
            item,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            with transaction.atomic():
                updated_item = serializer.save()
                serializer = ItemDetailSerializer(
                    updated_item,
                    context={
                        "request": request,
                    },
                )
                return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        item = Item.objects.get(pk=pk)
        if item.user != request.user:
            raise PermissionDenied
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ItemReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        item = self.get_object(pk)
        serializer = ReviewSerializer(
            item.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            new_review = serializer.save(
                user=request.user,
                item=self.get_object(pk),
            )
            serializer = ReviewSerializer(new_review)
            return Response(serializer.data)
        else:
            raise ParseError


class ItemPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            item = Item.objects.get(pk=pk)
            return item
        except Item.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        if request.user != self.get_object(pk).user:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(item=self.get_object(pk))
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            raise Response(serializer.errors)


class Tags(APIView):
    def get(self, request):
        try:
            tags = Tag.objects.all()
            serializer = TagSerializer(
                tags,
                many=True,
            )
            return Response(serializer.data)
        except Tag.DoesNotExist:
            raise NotFound
