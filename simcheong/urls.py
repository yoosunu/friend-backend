from django.urls import path
from .views import config

urlpatterns = [
    path("config/", config, name="simcheong-config"),
]
