from django.urls import path

from applications.profile.views import ProfileView, SingleAva

urlpatterns = [
    path("", ProfileView.as_view(), name="prof_index"),
    path("profile/<int:pk>/", SingleAva.as_view(), name="prof_avatar"),
]
