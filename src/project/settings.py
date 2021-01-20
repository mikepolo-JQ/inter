import os
from pathlib import Path

import dj_database_url
from django.urls import reverse_lazy
from dynaconf import settings as _ds

DIR_SRC = Path(__file__).resolve().parent.parent

DIR_PROJECT = (DIR_SRC / "project").resolve()

DIR_REPO = DIR_SRC.parent.resolve()


SECRET_KEY = _ds.SECRET_KEY

DEBUG = _ds.MODE_DEBUG

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    _ds.HOST,
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # -------------------------------------
    "applications.main.apps.LandingConfig",
    "applications.onboarding.apps.OnboardingConfig",
    "applications.profile.apps.ProfileConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [DIR_PROJECT / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

database_url = os.getenv("DATABASE_URL", _ds.DATABASE_URL)

DATABASES = {"default": dj_database_url.parse(database_url)}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ONBOARDING

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []

LOGIN_URL = reverse_lazy("onboarding:sign-in")
LOGIN_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = DIR_REPO / ".static"

STATICFILES_DIRS = [
    DIR_PROJECT / "static",
]

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "/images/"
MEDIA_ROOT = DIR_REPO / ".static/profiles/avatar"
