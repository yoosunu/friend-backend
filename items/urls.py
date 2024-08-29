from django.urls import path
from . import views

urlpatterns = [
    path("", views.Items.as_view()),
    path("<int:pk>", views.ItemDetail.as_view()),
    path("tags", views.Tags.as_view()),
    path("<int:pk>/reviews", views.ItemReviews.as_view()),
    path("<int:pk>/photos", views.ItemPhotos.as_view()),
]
