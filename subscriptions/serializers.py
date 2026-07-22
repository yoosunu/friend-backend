from rest_framework.serializers import ModelSerializer
from .models import Subs
from users.serializers import TinyUserSerializer


class SubscriptionSerializer(ModelSerializer):
    user = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Subs
        exclude = (
            "created_at",
            "updated_at",
        )
