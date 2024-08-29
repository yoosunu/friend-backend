from django.db import models
from common.models import CommonModel
from reviews.models import Review


# Create your models here.
class Item(CommonModel):
    """definition Item model config"""

    class languageChoices(models.TextChoices):
        C = ("c", "C")
        CPP = ("cpp", "CPP")
        PYTHON = ("python", "Python")
        JS = ("javascript", "Javascript")
        DART = ("dart", "Dart")
        JAVA = ("java", "Java")

    title = models.CharField(
        max_length=50,
        null=True,
    )

    description = models.TextField(
        null=True,
    )

    file = models.URLField(
        null=True,
        blank=True,
    )

    language = models.CharField(
        max_length=20,
        choices=languageChoices.choices,
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="items",
        null=True,
    )

    category = models.ForeignKey(
        "category.Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="items",
    )

    tags = models.ManyToManyField(
        "items.Tag",
        related_name="items",
    )

    def __str__(self) -> str:
        return self.title

    def rating_average(self):
        total_rating = 0
        reviews = Review.objects.filter(item=self)
        reviews_count = reviews.count()

        for review in reviews:
            total_rating += review.rating

        if reviews_count == 0:
            return "No Reviews"
        else:
            return round(total_rating / reviews_count, 1)


class Tag(CommonModel):

    class TagKindChoices(models.TextChoices):
        GAME = "game", "Game"
        UTIL = "util", "Util"
        HEALING = "healing", "Healing"

    tags = models.CharField(
        max_length=30,
        choices=TagKindChoices.choices,
        null=True,
    )

    def __str__(self) -> str:
        return self.tags
