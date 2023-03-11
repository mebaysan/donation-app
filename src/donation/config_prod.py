# Values are coming from docker-compose.yml
import os

from donation.settings import BASE_DIR

# App Variables to use in templates
APP_NAME = os.environ.get("APP_NAME")
APP_FAVICON_URL = os.environ.get("APP_FAVICON_URL")

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(" ")

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")

X_FRAME_OPTIONS = os.environ.get("X_FRAME_OPTIONS", "SAMEORIGIN") # DENY ALLOWALL SAMEORIGIN

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
    "payment_request_url": os.environ.get(
        "KUVEYTTURK_PAYMENT_REQUEST_URL"
    ),  # https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelPayGate
    "payment_approve_url": os.environ.get(
        "KUVEYTTURK_PAYMENT_APPROVE_URL"
    ),  # https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelProvisionGate
}

# JWT CONF
TOKEN_LIFETIME_HOURS = int(os.environ.get("TOKEN_LIFETIME_HOURS", 5))

# EMAIL
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True if os.environ.get("EMAIL_USE_TLS") == "True" else False
# EMAIL_USE_SSL = True if os.environ.get("EMAIL_USE_SSL") == 'True' else False

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
        },
    },
}
