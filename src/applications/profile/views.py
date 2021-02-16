from django.http import JsonResponse
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
from applications.profile.models import Rating


class ProfileView(CreateView):
    fields = ["content", "rating_value"]
    model = Feedback
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        pk = self.kwargs.get("pk", 0)
        profile = Profile.objects.filter(pk=pk).first()
        if not profile:
            raise ModuleNotFoundError(f"Profile with pk = {pk} not found...")

        context.update({"profile": profile})
        return context

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.author = self.request.user

        pk = self.kwargs.get("pk", 0)
        profile = Profile.objects.filter(pk=pk).first()

        if not profile:
            raise ModuleNotFoundError(f"Profile with pk = {pk} not found...")
        feedback.rating_id = profile.rating.pk

        rating_value = form.cleaned_data["rating_value"]
        profile.rating.value += rating_value
        profile.rating.save()

        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get("pk", 0)
        if not pk:
            raise ModuleNotFoundError(f"Profile with pk = {pk} not found...")
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
    fields = [
        "first_name",
        "last_name",
        "sity",
        "phone",
        "needed_help",
        "provide_help",
        "about",
    ]
    template_name = "profile/update_profile.html"

    def get_success_url(self):
        success_url = reverse_lazy("profile:profile", kwargs={"pk": self.object.pk})
        return success_url


class ContactListView(DetailView):
    model = Profile
    template_name = "profile/contacts.html"


class ContactReasonBackgroundView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        now_on_window_pk = kwargs.get("pk")
        now_on_window = Profile.objects.filter(pk=now_on_window_pk).first()

        payload = {"ok": False, "contact_reasons": 0, "reason": "unknown reason"}

        if not profile:
            payload.update({"reason": "profile not found"})

        contacts = profile.contacts.all()

        contacts_pk = [contact.pk for contact in contacts]

        reasons = {
            contact.pk: profile.get_contact_reason_with(contact) for contact in contacts
        }

        background = {contact.pk: contact.get_color for contact in contacts}

        payload.update(
            {
                "ok": True,
                "color_to_pk": now_on_window.get_color,
                "contacts_pk": contacts_pk,
                "contact_reasons": reasons,
                "contact_background": background,
                "reason": None,
            }
        )

        return JsonResponse(payload)


class ProfileCreateView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        pf = Profile(user=user)
        pf.save()
        rating = Rating(profile=pf)
        rating.save()

        redirect_url = reverse_lazy("profile:profile", kwargs={"pk": user.profile.pk})

        return redirect(redirect_url)
