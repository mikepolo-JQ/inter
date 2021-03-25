from django.urls import path

from src.applications.onboarding import views
from src.applications.onboarding.apps import OnboardingConfig

app_name = OnboardingConfig.label

urlpatterns = [
    path("sign-in/", views.SignInView.as_view(), name="sign-in"),
    path("sign-out/", views.SignOutView.as_view(), name="sign-out"),
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
]
