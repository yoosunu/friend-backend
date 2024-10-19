from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatRooms.as_view()),
    # path("<int:pk>", views.ChatRoomDetail.as_view()),
    path("@<str:name>", views.ChatsByChatRoom.as_view()),
]
