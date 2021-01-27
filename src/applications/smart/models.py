from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Match(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
