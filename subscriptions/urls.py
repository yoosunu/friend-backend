from django.urls import path
from . import views

from .views import debug_sub, force_migrate

urlpatterns = [
    path("", views.Subscription.as_view()),
    path("admin", views.SubscriptionsAdmin.as_view()),
    # path("admin", debug_sub, name="debug_sub"),
    path("force", force_migrate, name="force_migrate"),
]
