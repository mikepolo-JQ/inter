from django.apps import AppConfig


class ChatConfig(AppConfig):
    label = "chat"
    name = f"src.applications.{ label }"
