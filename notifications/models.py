from django.db import models
from common.models import CommonModel


# Create your models here.
class Notification(CommonModel):
    """notification model definition"""

    code = models.PositiveIntegerField(
        unique=True,
    )
    tag = models.CharField(
        max_length=100,
    )
    title = models.CharField(
        max_length=300,
    )
    link = models.CharField(
        max_length=400,
    )
    writer = models.CharField(
        max_length=100,
    )
    etc = models.CharField(
        max_length=100,
    )

    def __str__(self) -> str:
        return self.title
