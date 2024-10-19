from django.db import transaction
from .models import Chat, ChatRoom
from .serializers import (
    ChatDetailSerializer,
    ChatSerializer,
    ChatRoomsSerializer,
    ChatRoomDetailSerializer,
)
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    NotAuthenticated,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Create your views here.


class ChatRooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            chatrooms = ChatRoom.objects.filter(users=request.user)
            serializer = ChatRoomsSerializer(
                chatrooms,
                many=True,
            )
            return Response(serializer.data)
        except ChatRoom.DoesNotExist:
            raise NotFound

    def post(self, request):
        serializer = ChatRoomsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    new_chat_room = serializer.save(
                        owner=request.user,
                    )
                    users = request.data.get("users")
                    for user_pk in users:
                        user = User.objects.get(pk=user_pk)
                        new_chat_room.users.add(user)
                    serializer = ChatRoomsSerializer(new_chat_room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError
        else:
            return Response(serializer.errors)


# used real
class ChatsByChatRoom(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_chat_room(self, name):
        try:
            chatroom = ChatRoom.objects.get(name=name)
            return chatroom
        except ChatRoom.DoesNotExist or Chat.DoesNotExist:
            raise NotFound

    def get_object(self, name):
        try:
            chatroom = ChatRoom.objects.get(name=name)
            chats = Chat.objects.filter(chat_room=chatroom)
            return chats
        except Chat.DoesNotExist or Chat.DoesNotExist:
            raise NotFound

    def get(self, request, name):
        chats = self.get_object(name)
        serializer = ChatDetailSerializer(
            chats,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, name):
        serializer = ChatDetailSerializer(data=request.data)
        if serializer.is_valid():
            new_chat = serializer.save(
                user=request.user,
                chat_room=self.get_chat_room(name),
            )
            serializer = ChatDetailSerializer(new_chat)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, name):
        chat_room = self.get_chat_room(name)
        if chat_room.owner == request.user:
            chat_room.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        raise PermissionDenied
         

#don't use real
class ChatRoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            chatroom = ChatRoom.objects.get(pk=pk)
            return chatroom
        except ChatRoom.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        chatroom = self.get_object(pk)
        users = chatroom.users.all()
        usernames = []
        for user in users:
            usernames.append(str(user.username))
        username = str(request.user)
        if username in usernames or chatroom.owner == request.user:
            serializer = ChatRoomDetailSerializer(chatroom)
            return Response(serializer.data)
        else:
            raise NotAuthenticated

    def put(self, request, pk):
        chatroom = self.get_object(pk)
        if chatroom.owner != request.user:
            raise PermissionDenied
        serializer = ChatRoomDetailSerializer(
            chatroom,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_chatroom = serializer.save()
            return Response(ChatRoomDetailSerializer(updated_chatroom).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        chatroom = self.get_object(pk)
        if chatroom.owner == request.user:
            chatroom.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied
