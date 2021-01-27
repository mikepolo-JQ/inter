from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from project.settings import MEDIA_ROOT

User = get_user_model()


class Profile(models.Model):
    created_at = models.DateTimeField(default=datetime.now)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default="default_user.png")

    birth = models.DateTimeField(null=True, blank=True)
    sity = models.CharField(blank=True, null=True, max_length=30)
    phone = models.CharField(blank=True, null=True, max_length=20)
    needed_help_1 = models.TextField(blank=True, null=True)
    needed_help_2 = models.TextField(blank=True, null=True)
    needed_help_3 = models.TextField(blank=True, null=True)
    provide_help_1 = models.TextField(blank=True, null=True)
    provide_help_2 = models.TextField(blank=True, null=True)
    provide_help_3 = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    # def avatar_path(self):
    #     return str(MEDIA_ROOT / self.pk)
