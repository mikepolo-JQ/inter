from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.base import View

from applications.profile.models import Profile
from applications.smart.models import Contact
from applications.smart.models import Match
from applications.smart.utils import create_contacts
from applications.smart.utils import update_matches


class MatchListView(ListView):
    model = Match
    template_name = "smart/matches.html"


class ContactListView(ListView):
    model = Contact
    template_name = "smart/contacts.html"


class SmartStartView(View):
    def post(self, request, *args, **kwargs):

        profiles = Profile.objects.all()

        k_matches = update_matches(profiles)

        k_contact = create_contacts()

        payload = {
            "ok": True,
            "matches": f"{k_matches} new matches",
            "contacts": f"{k_contact} new contacts",
        }
        print(payload)

        return redirect("smart:contactList")


class DeleteAllMatches(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Match.objects.all().delete()
        return reverse_lazy("smart:matchList")


class DeleteAllContacts(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Contact.objects.all().delete()
        return reverse_lazy("smart:contactList")
