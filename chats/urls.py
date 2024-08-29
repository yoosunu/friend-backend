from django.urls import path
from . import views

urlpatterns = [
    path("chatrooms", views.ChatRooms.as_view()),
    path("chatrooms/<int:pk>", views.ChatRoomDetail.as_view()),
    path("@<str:name>", views.ChatsByChatRoom.as_view()),
]
