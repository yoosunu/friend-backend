from django.contrib import admin

from .models import Subs


# Register your models here.
@admin.register(Subs)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("safe_endpoint",)

    def safe_endpoint(self, obj):
        return obj.endpoint or "No Endpoint"

    safe_endpoint.short_description = "Endpoint"
