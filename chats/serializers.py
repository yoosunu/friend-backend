from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
)
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
    people = SerializerMethodField(
        read_only=True,
    )
    created_at = DateTimeField(
        format="%Y-%m-%d-%H:%M",
        read_only=True,
    )

    class Meta:
        model = Chat
        exclude = (
            "updated_at",
            "chat_room",
        )

    def get_people(self, chatRoom):
        return chatRoom.people()


class ChatRoomsSerializer(ModelSerializer):

    owner = ownerSerializer(
        read_only=True,
    )
    lastChat = SerializerMethodField(
        read_only=True,
    )
    hmp = SerializerMethodField(
        read_only=True,
    )
    people = SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = ChatRoom
        exclude = (
            "created_at",
            "updated_at",
        )

    def get_lastChat(self, chatRoom):
        return chatRoom.last_chat()

    def get_hmp(self, chatRoom):
        return chatRoom.hmp()

    def get_people(self, chatRoom):
        return chatRoom.people()


class ChatRoomDetailSerializer(ModelSerializer):

    users = TinyUserSerializer(
        read_only=True,
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
