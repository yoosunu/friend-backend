from rest_framework.serializers import ModelSerializer
from .models import Chat, ChatRoom
from users.serializers import TinyUserSerializer, ownerSerializer


class TinyChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ("name",)


class ChatSerializer(ModelSerializer):
    user = TinyUserSerializer(
        read_only=True,
    )
    chat_room = TinyChatRoomSerializer(
        read_only=True,
    )

    class Meta:
        model = Chat
        exclude = (
            "created_at",
            "updated_at",
        )


class ChatDetailSerializer(ModelSerializer):
    user = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Chat
        exclude = (
            "updated_at",
            "id",
            "chat_room",
        )


class ChatRoomsSerializer(ModelSerializer):

    owner = ownerSerializer(
        read_only=True,
    )

    class Meta:
        model = ChatRoom
        exclude = (
            "created_at",
            "updated_at",
        )


class ChatRoomDetailSerializer(ModelSerializer):

    users = TinyUserSerializer(
        many=True,
    )

    owner = ownerSerializer(
        read_only=True,
    )

    chats = ChatDetailSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ChatRoom
        exclude = (
            "created_at",
            "updated_at",
        )
