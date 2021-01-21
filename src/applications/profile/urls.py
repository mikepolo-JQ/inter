from django.urls import path

from applications.profile.views import ProfileView
from applications.profile.views import SingleAva

urlpatterns = [
    path("", ProfileView.as_view(), name="prof_index"),
    path("avatar/<int:pk>/", SingleAva.as_view(), name="prof_avatar"),
]
