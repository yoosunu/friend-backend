from django.db import models
from common.models import CommonModel


# Create your models here.
class Photo(CommonModel):
    file = models.URLField()
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    item = models.ForeignKey(
        "items.Item",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        return f"{self.item}/ {self.description}"


class Video(CommonModel):

    file = models.URLField()
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    item = models.OneToOneField(
        "items.Item",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.item}/ {self.description}"
