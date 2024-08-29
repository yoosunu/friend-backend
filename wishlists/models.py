from django.db import models
from common.models import CommonModel


# Create your models here.
class Wishlist(CommonModel):
    """wish list model definition"""

    name = models.CharField(
        max_length=150,
        null=True,
    )

    items = models.ManyToManyField(
        "items.Item",
        related_name="wishlists",
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    def __str__(self) -> str:
        return self.name
