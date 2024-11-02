from django.contrib import admin
from .models import Notification


# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "tag",
        "title",
        "link",
        "writer",
        "etc",
    )
