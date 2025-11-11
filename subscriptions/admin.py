from django.contrib import admin

from .models import Subs


# Register your models here.
@admin.register(Subs)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
