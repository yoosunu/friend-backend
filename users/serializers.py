from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "profile_image",
            "name",
        )


class ClassicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "profile_image",
            "name",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "id",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "id",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
            "last_login",
            "date_joined",
            "is_host",
        )


class ownerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "profile_image",
            "name",
        )
