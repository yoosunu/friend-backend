from django.urls import path
from . import views

urlpatterns = [
    path("", views.TDs.as_view()),
    path("<int:pk>", views.TD.as_view()),
    path("<int:pk>/tks", views.Tks.as_view()),
]
