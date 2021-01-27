from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from applications.smart import views

urlpatterns = [
    path("", views.SmartListView.as_view(), name="smartList"),
]
