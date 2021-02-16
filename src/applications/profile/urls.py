from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from applications.profile import views
from applications.profile.apps import ProfileConfig

app_name = ProfileConfig.label

urlpatterns = [
    path("my/", views.MyProfileView.as_view(), name="my"),
    path("<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("create/", views.ProfileCreateView.as_view(), name="profile_create"),
    path("sorry/", views.SorryView.as_view(), name="sorry_page"),
    path(
        "<int:pk>/update/",
        csrf_exempt(views.UpdateProfile.as_view()),
        name="update",
    ),
    path("<int:pk>/contacts/", views.ContactListView.as_view(), name="contactList"),
    path(
        "reasons_and_back/<int:pk>/", csrf_exempt(views.ContactReasonBackgroundView.as_view()), name="get_reasons_and_background"
    ),
]
