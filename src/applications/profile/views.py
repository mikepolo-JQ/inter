from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from applications.profile.models import Feedback
from applications.profile.models import Profile


class ProfileView(CreateView):
    fields = ["content", "rating_value"]
    model = Feedback
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        pk = self.kwargs.get("pk", 0)
        profile = Profile.objects.filter(pk=pk).first()
        if not profile:
            raise FileNotFoundError(f"Profile with pk = {pk} not found...")

        rating = profile.rating.value / (profile.rating.feedback_set.all().count() or 1)

        context.update({"profile": profile, "rating": "%.2f" % rating})
        return context

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.author = self.request.user

        pk = self.kwargs.get("pk", 0)
        profile = Profile.objects.filter(pk=pk).first()

        if not profile:
            raise FileNotFoundError(f"Profile with pk = {pk} not found...")
        feedback.rating_id = profile.rating.pk

        rating_value = form.cleaned_data["rating_value"]
        profile.rating.value += rating_value
        profile.rating.save()

        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get("pk", 0)
        if not pk:
            raise FileNotFoundError(f"Profile with pk = {pk} not found...")
        success_url = reverse_lazy("profile:profile", kwargs={"pk": pk})
        return success_url


class MyProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            "profile:profile", kwargs={"pk": self.request.user.profile.pk}
        )


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
