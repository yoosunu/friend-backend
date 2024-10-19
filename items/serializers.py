from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Item, Tag
from wishlists.models import Wishlist
from users.serializers import TinyUserSerializer
from medias.serializers import PhotoSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        exclude = (
            "created_at",
            "updated_at",
        )


class ItemListSerializer(ModelSerializer):

    class Meta:
        model = Item
        exclude = (
            "created_at",
            "updated_at",
        )

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    def get_rating(self, item):
        return item.rating_average()

    def get_is_owner(self, item):
        request = self.context["request"]
        return item.user == request.user

    def get_is_liked(self, item):
        request = self.context["request"]
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(
                    user=request.user,
                    items__pk=item.pk,
                ).exists()
        return False


class ItemDetailSerializer(ModelSerializer):

    user = TinyUserSerializer(
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
    )

    class Meta:
        model = Item
        exclude = (
            "created_at",
            "updated_at",
        )

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    is_wished = SerializerMethodField()

    def get_rating(self, item):
        return item.rating_average()

    def get_is_owner(self, item):
        request = self.context["request"]
        return item.user == request.user

    def get_is_wished(self, item):
        request = self.context["request"]
        if request.user.is_authenticated:
            return Wishlist.objects.filter(
                user=request.user,
                items__pk=item.pk,
            ).exists()
        return False

class ItemDetailSerializerForPut(ModelSerializer):

    user = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Item
        exclude = (
            "created_at",
            "updated_at",
        )

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )
    is_wished = SerializerMethodField()
    
    def get_rating(self, item):
        return item.rating_average()

    def get_is_owner(self, item):
        request = self.context["request"]
        return item.user == request.user

    def get_is_wished(self, item):
        request = self.context["request"]
        if request.user.is_authenticated:
            return Wishlist.objects.filter(
                user=request.user,
                items__pk=item.pk,
            ).exists()
        return False