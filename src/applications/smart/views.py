from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from applications.profile.models import Profile


class SmartListView(TemplateView):
    # model = Profile
    template_name = "smart/_base_smart.html"
