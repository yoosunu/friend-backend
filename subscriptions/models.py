from django.db import models
from common.models import CommonModel


# Create your models here.
class Subs(CommonModel):
    """subscription model definition"""

    endpoint = models.URLField()
    keys_auth = models.CharField(max_length=256)  # private key
    keys_p256dh = models.CharField(max_length=256)  # public key
