from django.apps import AppConfig


class ProfileConfig(AppConfig):
    label = "profile"
    name = f"applications.{ label }"
