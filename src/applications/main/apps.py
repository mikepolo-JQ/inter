from django.apps import AppConfig


class MainConfig(AppConfig):
    label = "main"
    name = f"src.applications.{ label }"
