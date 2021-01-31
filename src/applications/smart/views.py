from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic.base import View

from applications.profile.models import Profile
from applications.smart.models import Match


class SmartListView(ListView):
    model = Match
    template_name = "smart/_base_smart.html"


def key_sort(arg):
    return arg[0]


def searcher_matches(providers, needers):
    needers.sort(key=key_sort)
    save_needers = needers.copy()
    matches = []

    start = 0
    stop = len(needers) - 1

    for pr, pr_user in providers:

        while start <= stop:
            mid = (start + stop) // 2

            if pr == needers[mid][0]:
                match = (pr_user, needers[mid][1], pr)
                matches.append(match)
                needers.pop(mid)

                start = 0
                stop = len(needers) - 1
            elif pr < needers[mid][0]:
                stop = mid - 1
            else:
                start = mid + 1

        needers = save_needers.copy()
        start = 0
        stop = len(needers) - 1
    return matches


class SmartStartView(UpdateView):

    success_url = reverse_lazy("smartList")

    def post(self, request, *args, **kwargs):
        profiles = Profile.objects.all()

        providers = [(profile.provide_help, profile.user.pk) for profile in profiles]
        needers = [(profile.needed_help, profile.user.pk) for profile in profiles]

        matches = searcher_matches(providers, needers)

        k = 0
        for m in matches:
            provider_id, needer_id, reason = m

            if Match.objects.filter(provider_id=provider_id, needer_id=needer_id, reason=reason):
                continue

            match = Match(provider_id=provider_id, needer_id=needer_id, reason=reason)
            match.save()
            k += 1

        payload = {
            "ok": True,
            "data": f"You have {k} new matches",
        }
        return JsonResponse(payload)
