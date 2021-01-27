from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic import TemplateView

from applications.profile.models import Profile


class ProfileView(DetailView):
    model = Profile
    template_name = "profile/profile.html"


class UpdateProfile(UpdateView):
    model = Profile
    fields = ["birth", "phone", "sity"]
    template_name = "profile/update_profile.html"

    def get_success_url(self):
        success_url = reverse_lazy("profile", kwargs={"pk": self.object.pk})
        return success_url


class SingleAva(DetailView):
    model = Profile
    template_name = "profile/img.html"
