from django.contrib import admin

from src.applications.chat.models import Chat
from src.applications.chat.models import Message


@admin.register(Message)
class MessageAdminModel(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdminModel(admin.ModelAdmin):
    pass
