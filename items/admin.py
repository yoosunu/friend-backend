from django.contrib import admin
from .models import Item, Tag


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "language",
        "rating_average",
    )

    list_filter = ("language", "tags")

    search_fields = ("users" "tags",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
