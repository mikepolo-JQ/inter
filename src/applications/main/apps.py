from django.apps import AppConfig


class LandingConfig(AppConfig):
    # name = 'main'
    lable = "main"
    name = f"applications.{lable}"
