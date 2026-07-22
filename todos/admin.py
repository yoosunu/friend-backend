from django.contrib import admin
from .models import Everyday, Plan, Todo


# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    pass


@admin.register(Everyday)
class EverydayAdmin(admin.ModelAdmin):
    pass


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass
