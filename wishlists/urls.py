from django.urls import path
from . import views

urlpatterns = [
    path("", views.wishlists.as_view()),
    path("<int:pk>", views.wishlistDetail.as_view()),
    path("<int:pk>/items/<int:item_pk>", views.wishlistItem.as_view()),
]
