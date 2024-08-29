from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Photo


# Create your views here.
class PhotoDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            photo = Photo.objects.get(pk=pk)
            return photo
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if photo.item and photo.item.user != request.user:
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)
