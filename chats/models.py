from django.db import models
from common.models import CommonModel


# Create your models here.
class ChatRoom(CommonModel):
    name = models.CharField(
        max_length=50,
        null=True,
    )

    users = models.ManyToManyField(
        "users.User",
        related_name="chatrooms",
        null=True,
        blank=True,
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        if self.name != None:
            return self.name
        else:
            return "No Name"

    def people(self):
        return [user.username for user in self.users.all()]

    def hmp(self):
        return len(self.users.all())

    def last_chat(self):
        real_chats = []
        all_chats = Chat.objects.filter(chat_room=self)
        for chat in all_chats:
            real_chats.append(chat.chat)
        return real_chats[-1:]


class Chat(CommonModel):
    """friend model definition"""

    chat = models.TextField(
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="chats",
        null=True,
    )

    chat_room = models.ForeignKey(
        "chats.ChatRoom",
        on_delete=models.CASCADE,
        related_name="chats",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"[{self.user}] says: {self.chat}"

    def people(self):
        return self.chat_room.people()
