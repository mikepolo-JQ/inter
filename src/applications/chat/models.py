from datetime import datetime
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from dynaconf import ValidationError

User = get_user_model()


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=20, default="chat")
    talker = models.CharField(null=True, max_length=20, default="talker")

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

    @property
    def make_valid(self):
        if self.users.all().count() != 2:
            raise ValidationError(f"chat {self.name} does not have two user")
        return True

    def get_talker_for(self, user: User) -> User:
        if not self.make_valid:
            return None
        users = self.users.all()
        if user not in users:
            raise ValidationError(f"this user({user}) isn't in this chat({self.name})")
        talker = [tk for tk in users if tk is not user][0]
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)

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
