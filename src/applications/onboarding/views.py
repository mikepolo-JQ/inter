from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView


class SignInView(LoginView):
    template_name = "onboarding/sign-in.html"


class SignOutView(LogoutView):
    template_name = "onboarding/signed-out.html"


User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "username",
        )


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = "/"
    template_name = "onboarding/sign-up.html"

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]

        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)

        return super().form_valid(form)
