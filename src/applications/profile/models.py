from datetime import datetime
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models

from project.settings import MEDIA_ROOT

User = get_user_model()


class Profile(models.Model):

    created_at = models.DateTimeField(default=datetime.now)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default="default_user.png")

    sity = models.CharField(blank=True, null=True, max_length=30)
    phone = models.CharField(blank=True, null=True, max_length=20)

    needed_help = models.TextField(blank=True, null=True)
    provide_help = models.TextField(blank=True, null=True)

    contacts = models.ManyToManyField("self", related_name="contact_of")

    @property
    def get_contact_list(self) -> list:
        contact_list = list(self.contacts.all())
        return contact_list

    @property
    def get_chat_list(self) -> list:
        chat_list = list(self.user.chats.all())
        return chat_list

    def have_chat_with(self, user) -> bool:
        chat_list = self.get_chat_list
        for chat in chat_list:
            chat_users = chat.users.all()
            if user in chat_users:
                return True
        return False

    @property
    def feedback_list(self):
        fdb = list(self.rating.feedback_set.all())
        return fdb

    def __str__(self):
        return self.user.username

    # def avatar_path(self):
    #     return str(MEDIA_ROOT / self.pk)


class Rating(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    value = models.FloatField(default=0)

    def __str__(self):
        return f"{self.profile.user.username}"


class Feedback(models.Model):

    content = models.TextField(null=False, default="content")

    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    rating_value = models.IntegerField(default=0)

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
        return f"user:{self.author} feedback {self.rating.user}"

    class Meta:
        ordering = ["-created_at"]
