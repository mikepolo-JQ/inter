from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Match(models.Model):
    created_at = models.DateTimeField(default=datetime.now)

    provider = models.ForeignKey(
        User, related_name="provider", on_delete=models.CASCADE
    )
    needer = models.ForeignKey(User, related_name="needer", on_delete=models.CASCADE)

    reason = models.TextField(null=False, default="reason")

    def person_is_first(self, user) -> bool:
        return Match.objects.filter(pk=self.pk, first_user=user).exists()
