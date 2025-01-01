from django.db import models
from common.models import CommonModel


# Create your models here.
class Notification(CommonModel):
    """notification model definition"""

    code = models.PositiveIntegerField(
        unique=True,
    )
    tag = models.CharField(
        max_length=1000,
    )
    title = models.CharField(
        max_length=1000,
    )
    link = models.CharField(
        max_length=1000,
    )
    writer = models.CharField(
        max_length=1000,
    )
    etc = models.CharField(
        max_length=1000,
    )

    def __str__(self) -> str:
        return self.title
