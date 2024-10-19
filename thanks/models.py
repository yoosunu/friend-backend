from django.db import models
from common.models import CommonModel


# Create your models here.
class ThanksDate(CommonModel):
    preview = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="thanksdates",
    )

    diary = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.preview


class Thank(CommonModel):
    payload = models.CharField(
        max_length=100,
        null=True,
    )

    thanksDate = models.ForeignKey(
        "thanks.ThanksDate",
        on_delete=models.CASCADE,
        related_name="thanks",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="thanks",
    )

    def __str__(self) -> str:
        return self.payload
