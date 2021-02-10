from datetime import datetime

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

    def __str__(self):
        return self.user.username

    # def avatar_path(self):
    #     return str(MEDIA_ROOT / self.pk)
