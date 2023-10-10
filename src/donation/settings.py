"""
Django settings for donation project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = int(os.environ.get("DEBUG", default=0))
if DEBUG == 1:
    DEBUG = True
else:
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
    "rangefilter",
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

LANGUAGE_CODE = "tr-TR"

TIME_ZONE = "Europe/Istanbul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/django-static/"  # for proxy purposes
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/django-media/"  # for proxy purposes

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
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    # "PAGE_SIZE": 20,
}

# App Variables to use in templates
APP_NAME = os.environ.get("APP_NAME")
APP_FAVICON_URL = os.environ.get("APP_FAVICON_URL")

# this will be used in payment success and fail urls to redirect user from payment page to cart page
APP_PAYMENT_RESPONSE_URL = os.environ.get("APP_PAYMENT_RESPONSE_URL")

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(" ")

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")

# DENY ALLOWALL SAMEORIGIN
X_FRAME_OPTIONS = os.environ.get("X_FRAME_OPTIONS", "SAMEORIGIN")

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True if os.environ.get("SECURE_SSL_REDIRECT") == "True" else False

SESSION_COOKIE_SECURE = (
    True if os.environ.get("SESSION_COOKIE_SECURE") == "True" else False
)

CSRF_COOKIE_SECURE = True if os.environ.get("CSRF_COOKIE_SECURE") == "True" else False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

# Media root for prod mode
MEDIA_ROOT = BASE_DIR / "media"

# KUVEYTTURK CONF
KUVEYTTURK_CONF = {
    "store_no": os.environ.get("KUVEYTTURK_STORE_NO"),
    "customer_no": os.environ.get("KUVEYTTURK_CUSTOMER_NO"),
    "username": os.environ.get("KUVEYTTURK_USERNAME"),
    "password": os.environ.get("KUVEYTTURK_PASSWORD"),
    "ok_url": os.environ.get("KUVEYTTURK_OK_URL"),
    "fail_url": os.environ.get("KUVEYTTURK_FAIL_URL"),
    # https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelPayGate
    "payment_request_url": os.environ.get("KUVEYTTURK_PAYMENT_REQUEST_URL"),
    # https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelProvisionGate
    "payment_approve_url": os.environ.get("KUVEYTTURK_PAYMENT_APPROVE_URL"),
}

# JWT CONF
TOKEN_LIFETIME_HOURS = int(os.environ.get("TOKEN_LIFETIME_HOURS", 5))
JWT_CONF = {"TOKEN_LIFETIME_HOURS": TOKEN_LIFETIME_HOURS}

# EMAIL
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True if os.environ.get("EMAIL_USE_TLS") == "True" else False
EMAIL_USE_SSL = True if os.environ.get("EMAIL_USE_SSL") == "True" else False

CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

# LOGGING
if DEBUG is False:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"},
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
            "file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": "/var/log/donation/donation.log",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": True,
            },
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": "WARNING",
                "propagate": True,
            },
            "donation": {
                "handlers": ["console", "file"],
                "level": "ERROR",
                "propagate": True,
            },
        },
    }
