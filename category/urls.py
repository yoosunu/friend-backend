from django.urls import path
from . import views

urlpatterns = [
    path("", views.Categories.as_view()),
]
