from django.apps import AppConfig


class ProfileConfig(AppConfig):
    label = "profile"
    name = f"src.applications.{ label }"
