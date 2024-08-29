from django.db import models
from common.models import CommonModel


# Create your models here.
class Review(CommonModel):
    review = models.TextField()

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

    rating = models.PositiveIntegerField(
        null=True,
        # max_value should be included.
    )

    def __str__(self) -> str:
        return f"{self.user} reviewed this item."
