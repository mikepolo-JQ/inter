from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from project.settings import MEDIA_ROOT

User = get_user_model()


class Profile(models.Model):
    created_at = models.DateTimeField(default=datetime.now)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default="default_user.png")

    def __str__(self):
        return self.user.username

    # def avatar_path(self):
    #     return str(MEDIA_ROOT / self.pk)
