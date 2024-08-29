from django.db import models
from common.models import CommonModel


# Create your models here.
class Category(CommonModel):

    class CategoryKindChoice(models.TextChoices):
        item = ("item", "Item")
        chat = ("chat", "Chat")

    kind = models.CharField(
        max_length=30,
        choices=CategoryKindChoice.choices,
    )

    def __str__(self) -> str:
        return self.kind

    class Meta:
        verbose_name_plural = "Categories"
