# my_project/__init__.py

from .celery import app as celery_app

__all__ = ("celery_app",)

from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


def create_superuser():
    User.objects.create_superuser("yoosunu", "yoosunu010@naver.com", "yoo010212??!")


create_superuser()
