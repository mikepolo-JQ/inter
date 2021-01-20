from django.urls import path

from applications.profile.views import ProfileView

urlpatterns = [
    path("", ProfileView.as_view(), name="prof_index"),
]
