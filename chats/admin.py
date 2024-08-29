from django.contrib import admin
from .models import Chat, ChatRoom


# Register your models here.
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "people",
    )


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "chat",
        "created_at",
    )
