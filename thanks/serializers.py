from rest_framework.serializers import ModelSerializer
from .models import ThanksDate, Thank
from users.serializers import TinyUserSerializer


class TinyThanksDateSerializer(ModelSerializer):

    class Meta:
        model = ThanksDate
        fields = ("preview",)


class ThanksDateSerializer(ModelSerializer):

    user = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = ThanksDate
        fields = "__all__"


class ThanksSerializer(ModelSerializer):

    thanksDate = TinyThanksDateSerializer(
        read_only=True,
    )

    class Meta:
        model = Thank
        fields = (
            "id",
            "thanksDate",
            "payload",
        )
