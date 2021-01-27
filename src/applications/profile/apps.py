from django.apps import AppConfig


class ProfileConfig(AppConfig):
    # name = 'main'
    lable = "profile"
    name = f"applications.{lable}"
