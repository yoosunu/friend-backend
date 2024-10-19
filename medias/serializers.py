from rest_framework.serializers import ModelSerializer
from .models import Photo, Video


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "id",
            "file",
            "description",
        )


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "id",
            "file",
            "description",
        )
