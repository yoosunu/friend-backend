from django.contrib import admin
from .models import Friend


# Register your models here.
@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    pass
