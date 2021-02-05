from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView, RedirectView

from applications.profile.models import Profile


class ProfileView(DetailView):
    model = Profile
    template_name = "profile/profile.html"


class MyProfileView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy("profile:profile", kwargs={"pk": request.user.pk}))


class SorryView(TemplateView):
    template_name = "profile/sorry.html"


class UpdateProfile(UpdateView):
    model = Profile
    fields = ["sity", "phone", "needed_help", "provide_help"]
    template_name = "profile/update_profile.html"

    def get_success_url(self):
        success_url = reverse_lazy("profile:profile", kwargs={"pk": self.object.pk})
        return success_url


class ContactListView(DetailView):
    model = Profile
    template_name = "smart/contacts.html"
