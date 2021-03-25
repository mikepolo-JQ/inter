from django.apps import AppConfig


class OnboardingConfig(AppConfig):
    label = "onboarding"
    name = f"src.applications.{ label }"
