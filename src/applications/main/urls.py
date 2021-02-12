from django.urls import path

from applications.main.apps import MainConfig
from applications.main.views import IndexView

app_name = MainConfig.label

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
