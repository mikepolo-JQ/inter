from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include("applications.main.urls"), name="index"),
    path("o/", include("applications.onboarding.urls"), name="onboarding"),
    path("profile/", include("applications.profile.urls"), name="profile"),
]
