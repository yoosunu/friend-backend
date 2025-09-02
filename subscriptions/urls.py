from django.urls import path
from . import views
from .views import debug_sub

urlpatterns = [
    path("", views.Subscription.as_view()),
    # path("admin", views.SubscriptionsAdmin.as_view()),
    path("admin", debug_sub, name="debug_sub"),
]
