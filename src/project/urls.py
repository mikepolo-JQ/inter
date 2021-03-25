import sys
import traceback

from django.conf import settings
from django.conf.urls import handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import include
from django.urls import path
from django.views.defaults import ERROR_500_TEMPLATE_NAME
from dynaconf import settings as _ds


def handle_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    traceback.print_exc()

    error_class, error, tb = sys.exc_info()

    context = {
        "traceback": traceback.walk_tb(tb),
        "HOST": _ds.HOST,
        "error_name": error_class.__name__,
        "error": error,
    }

    payload = render(request, template_name, context=context)

    return HttpResponse(payload, status=500)


handler500 = handle_error


def make_error(_request):
    1 / 0


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include("main.urls"), name="index"),
    path("o/", include("onboarding.urls"), name="onboarding"),
    path("profile/", include("profile.urls"), name="profile"),
    path("smart/", include("smart.urls"), name="smart"),
    path("messenger/", include("chat.urls"), name="chat"),
    path("e/", make_error),
    path("accounts/", include("allauth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
