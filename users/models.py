from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    profile_image = models.URLField(blank=True)

    name = models.CharField(
        max_length=150,
        default="",
        blank=True,
    )
    is_host = models.BooleanField(
        null=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=20,
        choices=LanguageChoices.choices,
    )
