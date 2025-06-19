from rest_framework.serializers import ModelSerializer
from .models import Subscription
from users.serializers import TinyUserSerializer


class SubscriptionSerializer(ModelSerializer):
    user = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Subscription
        exclude = (
            "created_at",
            "updated_at",
        )
