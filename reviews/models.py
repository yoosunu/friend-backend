from django.db import models
from common.models import CommonModel


# Create your models here.
class Review(CommonModel):
    review = models.TextField()

    rating = models.PositiveIntegerField()

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        related_name="reviews",
    )

    item = models.ForeignKey(
        "items.Item",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    def __str__(self) -> str:
        return f"{self.user} reviewed this item."
