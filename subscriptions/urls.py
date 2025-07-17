from django.urls import path
from . import views

urlpatterns = [
    path("", views.Subscription.as_view()),
    path("admin", views.SubscriptionsAdmin.as_view()),
]
