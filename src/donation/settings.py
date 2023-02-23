"""
Django settings for donation project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = int(os.environ.get("DEBUG", default=0))
if DEBUG == 1:
    from .config_dev import *

    DEBUG = True
elif DEBUG == 2:
    from .config_dev import *

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    DEBUG = True
else:
    from .config_prod import *

    DEBUG = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party packages
    "rest_framework",
    "corsheaders",
    # custom apps
    "apps.management.apps.ManagementConfig",
    "apps.donor.apps.DonorConfig",
    "apps.payment.apps.PaymentConfig",
    "apps.web.apps.WebConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "donation.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "helpers.context_processors.get_app_name",
                "helpers.context_processors.get_favicon",
            ],
        },
    },
]

WSGI_APPLICATION = "donation.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-EN"

TIME_ZONE = "Europe/Istanbul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/django-static/" # for proxy purposes
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/django-media/" # for proxy purposes

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_TAGS = {
    messages.ERROR: "danger",
    messages.WARNING: "warning",
    messages.SUCCESS: "success",
    messages.INFO: "info",
    "my_message_class": "custom",
}

# custom user model
AUTH_USER_MODEL = "management.User"

# Media URL
MEDIA_URL = "/media/"

LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/"

# REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.management.authentication.JWTAuthentication",
    ],
}

JWT_CONF = {"TOKEN_LIFETIME_HOURS": TOKEN_LIFETIME_HOURS}
