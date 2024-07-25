from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.
class MyUser(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        related_name="myuser_set",  # Change this to avoid clash
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="myuser_permissions_set",  # Change this to avoid clash
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    # last and first name are also have to have default value. But I didn't typed. why?
    # cause I assigned it when I create the user at the beginning.
    # But the name and is_host below, created when the user was already made.
    # so, I had to assign the default value.
    name = models.CharField(
        max_length=150,
        default="",
        blank=True,
    )
    is_host = models.BooleanField(
        null=True,
    )
    # avatar = models.ImageField()
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
