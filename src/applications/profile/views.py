from django.views.generic import TemplateView, DetailView

from applications.profile.models import Profile


class ProfileView(TemplateView):
    template_name = "profile/index.html"
    model = Profile


class SingleAva(DetailView):
    model = Profile
    template_name = "profile/img.html"
