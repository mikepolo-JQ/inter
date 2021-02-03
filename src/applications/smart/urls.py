from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from applications.smart import views
from applications.smart.apps import SmartConfig

app_name = SmartConfig.label

urlpatterns = [
    path("matches/", views.MatchListView.as_view(), name="matchList"),
    path("start/", csrf_exempt(views.SmartStartView.as_view()), name="smartStart"),
    path("contacts/", views.ContactListView.as_view(), name="contactList"),
    path(
        "matches/delete/", views.DeleteAllMatches.as_view(), name="delete_all_matches"
    ),
    path(
        "contacts/delete/",
        views.DeleteAllContacts.as_view(),
        name="delete_all_contacts",
    ),
]
