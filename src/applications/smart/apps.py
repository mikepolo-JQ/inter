from django.apps import AppConfig


class SmartConfig(AppConfig):
    label = "smart"
    name = f"applications.{ label }"
