from datetime import datetime
from datetime import timedelta
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import models
from dynaconf import ValidationError

from profile.models import Profile

User = get_user_model()


class Chat(models.Model):
    name = models.CharField(null=False, max_length=50, default="chat")
    talker = models.ForeignKey(Profile, on_delete=models.CASCADE)

    profiles = models.ManyToManyField(
        Profile,
        related_name="chats",
        null=False,
    )

    @classmethod
    def create(cls, p, user_p):
        ch = cls(name=f"{p}|{user_p}")
        ch.talker = p
        ch.save()
        ch.profiles.add(p, user_p)
        return ch

    @property
    def make_valid(self):
        if self.profiles.all().count() != 2:
            raise ValidationError(f"chat {self.name} does not have two user")
        return True

    def get_talker_for(self, user: Profile) -> Optional[Profile]:
        if not self.make_valid:
            return None
        users = self.profiles.all()
        if user not in users:
            raise ValidationError(
                f"this profile({user}) isn't in this chat({self.name})"
            )

        talker = [tk for tk in users if tk != user][0]
        return talker

    @property
    def last_message(self):
        self.message_set.update()
        last = self.message_set.all().last()
        return last

    @property
    def message_list(self) -> list:
        return list(self.message_set.all())

    def __str__(self):
        return f"{self.name}"


class Message(models.Model):
    created_at = models.DateTimeField(default=datetime.now)

    content = models.TextField(null=False, default="content")

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    @property
    def format_date(self) -> str:
        return self.created_at.strftime("%d.%m.%Y")

    @property
    def format_time(self) -> str:
        return self.created_at.strftime("%H:%M")

    @property
    def get_datetime(self):
        today = datetime.now().date()
        msg_date = self.created_at.date()
        yesterday = today - timedelta(1)

        if msg_date < yesterday:
            dt = f"{self.format_date} {self.format_time}"
        elif today > msg_date:
            dt = f"Вчера {self.format_time}"
        else:
            dt = f"{self.format_time}"

        return dt

    def __str__(self):
        return f"user:{self.author} in {self.created_at}"

    class Meta:
        ordering = ["created_at"]
