from django.contrib import admin
from .models import Wishlist


# Register your models here.
@admin.register(Wishlist)
class wishlistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
    )
