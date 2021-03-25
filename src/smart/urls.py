from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from smart import views
from smart.apps import SmartConfig

app_name = SmartConfig.name

urlpatterns = [
    path("matches/<int:pk>/", views.MatchListView.as_view(), name="matchList"),
    path("start/", csrf_exempt(views.SmartStartView.as_view()), name="smartStart"),
    path(
        "start/su/", csrf_exempt(views.BIGSmartUpdateView.as_view()), name="bigUpdate"
    ),
    path(
        "matches/delete/", views.DeleteAllMatches.as_view(), name="delete_all_matches"
    ),
    path(
        "contacts/delete/",
        views.DeleteContacts.as_view(),
        name="delete_all_contacts",
    ),
]
