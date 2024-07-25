from django.db import models
from common.models import CommonModel


# Create your models here.
class Friend(CommonModel):
    """friend model definition"""

    chat = models.TextField(
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        "users.MyUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"[{self.user}] says: {self.chat}"
