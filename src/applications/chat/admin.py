from django.contrib import admin

from applications.chat.models import Chat
from applications.chat.models import Message


@admin.register(Message)
class MessageAdminModel(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdminModel(admin.ModelAdmin):
    pass
