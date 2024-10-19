from django.db import models
from common.models import CommonModel


# Create your models here.


class Todo(CommonModel):
    name = models.CharField(max_length=50)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="todos",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name


class Everyday(CommonModel):
    name = models.CharField(
        max_length=50,
        null=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="everydays",
        blank=True,
        null=True,
    )

    todo = models.ForeignKey(
        "todos.Todo",
        on_delete=models.CASCADE,
        related_name="everydays",
        blank=True,
        null=True,
    )

    time = models.TimeField(
        blank=True,
        null=True,
    )

    done = models.BooleanField(
        default=False,
    )

    def __str__(self) -> str:
        return self.name


class Plan(CommonModel):
    name = models.CharField(
        max_length=50,
        null=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="plans",
        blank=True,
        null=True,
    )

    todo = models.ForeignKey(
        "todos.Todo",
        on_delete=models.CASCADE,
        related_name="plans",
        blank=True,
        null=True,
    )

    description = models.TextField(
        null=True, 
        blank=True,
    )

    time = models.DateTimeField(
        blank=True,
        null=True,
    )

    done = models.BooleanField(
        default=False,
    )

    def __str__(self) -> str:
        return self.name
