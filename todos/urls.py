from django.urls import path
from . import views

urlpatterns = [
    path("", views.Todos.as_view()),
    path("<int:pk>", views.TodoDetail.as_view()),
    path("<int:pk>/everydays", views.EveryDays.as_view()),
    path("<int:pk>/everydays/<int:pk_>", views.EveryDay.as_view()),
    path("<int:pk>/plans", views.Plans.as_view()),
    path("<int:pk>/plans/<int:pk_>", views.PlanDetail.as_view()),
]
