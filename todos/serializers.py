from rest_framework.serializers import ModelSerializer
from .models import Todo, Everyday, Plan
from users.serializers import TinyUserSerializer


class EverydaySerializer(ModelSerializer):

    class Meta:
        model = Everyday
        fields = (
            "id",
            "name",
            "time",
            "done",
        )


class PlanSerializer(ModelSerializer):

    class Meta:
        model = Plan
        fields = (
            "id",
            "name",
            "time",
            "description",
            "done",
        )


class TodoSerializer(ModelSerializer):
    user = TinyUserSerializer(
        read_only=True,
    )
    everydays = EverydaySerializer(
        many=True,
        required=False,
    )

    plans = PlanSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Todo
        exclude = (
            "created_at",
            "updated_at",
        )
