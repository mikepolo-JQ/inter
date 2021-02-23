from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.base import View

from applications.profile.models import Profile
from applications.smart.models import Match
from applications.smart.utils import create_contacts
from applications.smart.utils import search_contacts_for
from applications.smart.utils import update_matches


class MatchListView(ListView):
    model = Match
    template_name = "smart/matches.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        pk = self.kwargs.get("pk", 0)
        matches = list(Match.objects.filter(needer_id=pk))
        matches += Match.objects.filter(provider_id=pk)
        context.update({"matches": matches})
        return context


class SmartStartView(RedirectView):
    http_method_names = ["post"]

    def get_redirect_url(self, *args, **kwargs):

        profile = self.request.user.profile
        k_contact = search_contacts_for(profile)

        payload = {
            "ok": True,
            "contacts": f"{k_contact} new contacts",
        }
        print(payload)

        redirect_url = reverse_lazy("profile:contactList", kwargs={"pk": profile.pk})
        return redirect_url


class BIGSmartUpdateView(RedirectView):
    http_method_names = ["post"]

    def get_redirect_url(self, *args, **kwargs):

        k_matches = update_matches()

        k_contact = create_contacts()

        payload = {
            "ok": True,
            "matches": f"{k_matches} new matches",
            "contacts": f"{k_contact} new contacts",
        }
        print(payload)

        redirect_url = reverse_lazy("smart:matchList")
        return redirect(redirect_url)


class DeleteAllMatches(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Match.objects.all().delete()
        return reverse_lazy("smart:matchList")


class DeleteContacts(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get("pk", 0)
        if pk:
            person = Profile.objects.get(pk)
            person.contacts.clear()
            redirect_url = reverse_lazy("profile:contactList", kwargs={"pk": pk})
        else:
            redirect_url = reverse_lazy("smart:matchList")
        return redirect_url
