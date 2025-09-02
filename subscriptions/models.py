from django.db import models
from common.models import CommonModel


# Create your models here.
class Subs(CommonModel):
    """subscription model definition"""

    endpoint = models.URLField(
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
        return self.endpoint
