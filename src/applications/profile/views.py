from django.views.generic import DetailView
from django.views.generic import TemplateView

from applications.profile.models import Profile


class ProfileView(TemplateView):
    template_name = "profile/index.html"


class SingleAva(DetailView):
    model = Profile
    template_name = "profile/img.html"
