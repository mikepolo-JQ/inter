from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    created_at = models.DateTimeField(default=datetime.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username
