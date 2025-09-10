from django.db import models
from common.models import CommonModel


# Create your models here.
class Subs(CommonModel):
    """subscription model definition"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    endpoint = models.TextField(
        null=True,
        blank=True,
    )
    keys_auth = models.TextField(
        null=True,
        blank=True,
    )  # private key
    keys_p256dh = models.TextField(
        null=True,
        blank=True,
    )  # public key

    def __str__(self):
        return self.endpoint or "No Endpoint"
