from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Review
from users.serializers import TinyUserSerializer


class ReviewSerializer(ModelSerializer):

    user = TinyUserSerializer(
        read_only=True,
    )

    is_owner = SerializerMethodField()

    def get_is_owner(self, review):
        request = self.context["request"]
        return review.user == request.user

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "review",
            "rating",
            "is_owner",
        )
