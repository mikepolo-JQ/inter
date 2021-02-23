from datetime import datetime
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models

from applications.smart.models import Match

User = get_user_model()


class Profile(models.Model):

    created_at = models.DateTimeField(default=datetime.now)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default="default_user.png")
    first_name = models.CharField(null=False, max_length=30, default="name")
    last_name = models.CharField(null=False, max_length=30, default="last_name")

    sity = models.CharField(null=False, default="", max_length=30)
    phone = models.CharField(null=False, default="", max_length=20)

    needed_help = models.TextField(
        null=False,
        default="",
    )
    provide_help = models.TextField(
        null=False,
        default="",
    )

    active = models.BooleanField(default=False)
    contacts = models.ManyToManyField("self", related_name="contact_of")
    about = models.TextField(null=True, blank=True)

    def have_chat_with(self, profile) -> int:
        chat_list = self.chats.all()
        for chat in chat_list:
            chat_users = chat.profiles.all()
            if profile in chat_users:
                return chat.pk
        return 0

    @property
    def get_rating(self):
        rating = self.rating.value / (self.rating.feedback_set.all().count() or 1)
        return "%.2f" % rating

    @property
    def get_color(self):
        rating = self.rating.value / (self.rating.feedback_set.all().count() or 1)
        if rating < 3:
            return "red"
        elif rating < 4:
            return "yellow"
        else:
            return "green"

    def get_contact_reason_with(self, other):
        match = Match.objects.filter(provider=other.user, needer=self.user).first()
        return match.reason

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["-created_at"]


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


class TemporaryProfile(models.Model):
    profile = models.ForeignKey(Profile, related_name="copy", on_delete=models.CASCADE)
    needed_help = models.TextField(
        null=False,
        default="",
    )
    provide_help = models.TextField(
        null=False,
        default="",
    )
