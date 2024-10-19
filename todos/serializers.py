from rest_framework.serializers import ModelSerializer
from .models import Todo, Everyday, Plan
from users.serializers import TinyUserSerializer


class EverydaySerializer(ModelSerializer):

    class Meta:
        model = Everyday
        fields = (
            "name",
            "time",
            "done",
        )


class PlanSerializer(ModelSerializer):

    class Meta:
        model = Plan
        fields = (
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
    )

    plans = PlanSerializer(
        many=True,
    )

    class Meta:
        model = Todo
        fields = "__all__"
