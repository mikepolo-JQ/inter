from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from applications.profile import views
from applications.profile.apps import ProfileConfig

app_name = ProfileConfig.label

urlpatterns = [
    path("<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path(
        "<int:pk>/update/",
        csrf_exempt(views.UpdateProfile.as_view()),
        name="update_profile",
    ),
    path("avatar/<int:pk>/", views.SingleAva.as_view(), name="profile_avatar"),
]
