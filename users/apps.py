from django.apps import AppConfig
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        if not User.objects.filter(username="yoosunu").exists():
            User.objects.create_superuser(
                "yoosunu", "yoosunu010@naver.com", "yoo010212??!"
            )
