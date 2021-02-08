from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from dynaconf import ValidationError

User = get_user_model()


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=20, default="chat")

    users = models.ManyToManyField(
        User,
        related_name="chats",
        null=False,
    )

    @classmethod
    def create(cls, u1, u2):
        ch = cls(name=f"{u1} and {u2}")
        ch.save()
        ch.users.add(u1, u2)
        return ch

    def __str__(self):
        return f"{self.name}"


class Message(models.Model):
    created_at = models.DateTimeField(default=datetime.now)

    content = models.TextField(null=False, default="content")

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_date_of_creation(self):
        self.created_at.strftime('%d.%m.%Y')

    @property
    def get_time_of_creation(self):
        self.created_at.strftime('%H:%M:%S')

    def __str__(self):
        return f"user:{self.author} in {self.created_at}"
