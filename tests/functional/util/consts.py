# from django.urls import reverse_lazy
#
# from applications.profile.models import Profile
# from tests.functional.util.actions.onboarding import Credentials

URL_SERVICE = "http://localhost:8000"

URL_LANDING = f"{URL_SERVICE}/"

URL_SIGN_IN = f"{URL_SERVICE}/o/sign-in/"
URL_SIGN_OUT = f"{URL_SERVICE}/o/sign-out/"
URL_SIGN_UP = f"{URL_SERVICE}/o/sign-up/"

URL_MATCHES_LIST = f"{URL_SERVICE}/smart/matches/"

URL_MY_PROFILE = f"{URL_SERVICE}/profile/my/"


# def get_profile_url(credentials: Credentials):
#     profile = Profile.objects.get(username=credentials.username)
#     URL_PROFILE = reverse_lazy("profile:profile", kwargs={"pk": profile.pk})
#     return URL_PROFILE
