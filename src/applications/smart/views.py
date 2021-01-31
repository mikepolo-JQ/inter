from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.base import View

from applications.profile.models import Profile
from applications.smart.models import Contact
from applications.smart.models import Match
from applications.smart.utils import create_contacts
from applications.smart.utils import searcher_matches
from applications.smart.utils import start_filter


class MatchListView(ListView):
    model = Match
    template_name = "smart/matches.html"


class ContactListView(ListView):
    model = Contact
    template_name = "smart/contacts.html"


class SmartStartView(View):
    def post(self, request, *args, **kwargs):

        profiles = Profile.objects.all()
        providers = start_filter(
            [[profile.provide_help, profile.user.pk] for profile in profiles]
        )
        needers = start_filter(
            [[profile.needed_help, profile.user.pk] for profile in profiles]
        )

        print(f"providers after filter {providers}")
        print(f"needers after filter {needers}")
        matches = searcher_matches(providers, needers)

        k = 0
        for m in matches:
            provider_id, needer_id, reason = m

            if Match.objects.filter(
                provider_id=provider_id, needer_id=needer_id, reason=reason
            ):
                continue

            match = Match(provider_id=provider_id, needer_id=needer_id, reason=reason)
            match.save()
            k += 1

        k_contact = create_contacts()

        payload = {
            "ok": True,
            "matches": f"{k} new matches",
            "contacts": f"{k_contact} new contacts",
        }
        print(payload)

        return redirect("smart:contactList")
