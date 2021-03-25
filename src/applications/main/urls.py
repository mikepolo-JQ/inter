from django.urls import path

from src.applications.main.apps import MainConfig
from src.applications.main.views import IndexView

app_name = MainConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
