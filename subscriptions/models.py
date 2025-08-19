from django.db import models
from common.models import CommonModel


# Create your models here.
class Subs(CommonModel):
    """subscription model definition"""

    endpoint = models.URLField()
    keys_auth = models.CharField(max_length=256)  # private key
    keys_p256dh = models.CharField(max_length=256)  # public key

    def __str__(self) -> str:
        return self.endpoint


# .env에 저장된 그 키 받는 게 배포 과정에서 안되는듯.
