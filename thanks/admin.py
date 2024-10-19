from django.contrib import admin
from .models import ThanksDate, Thank


# Register your models here.
@admin.register(ThanksDate)
class ThanksDateAdmin(admin.ModelAdmin):
    pass


@admin.register(Thank)
class ThankAdmin(admin.ModelAdmin):
    pass
