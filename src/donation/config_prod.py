# Values are coming from docker-compose.yml
import os

from donation.settings import BASE_DIR

# App Variables to use in templates
APP_NAME = os.getenv("APP_NAME")
APP_FAVICON_URL = os.getenv("APP_FAVICON_URL")

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

# CORS_ALLOWED_ORIGINS = []

# CSRF_TRUSTED_ORIGINS = []

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
    }
}

# APP MEDIA STORAGE TYPE
APP_MEDIA_STORAGE_TYPE = os.getenv("APP_MEDIA_STORAGE_TYPE")  # set 'S3' to use S3

if APP_MEDIA_STORAGE_TYPE == 'ON_PREM':
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    MEDIA_ROOT = BASE_DIR / 'media'

# KUVEYTTURK CONF
KUVEYTTURK_CONF = {
    'store_no': os.getenv('KUVEYTTURK_STORE_NO'),
    'customer_no': os.getenv('KUVEYTTURK_CUSTOMER_NO'),
    'username': os.getenv('KUVEYTTURK_USERNAME'),
    'password': os.getenv('KUVEYTTURK_PASSWORD'),
    'ok_url': os.getenv('KUVEYTTURK_OK_URL'),
    'fail_url': os.getenv('KUVEYTTURK_FAIL_URL'),
    'payment_request_url': 'https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelPayGate',
    'payment_approve_url': 'https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelProvisionGate',
}

# JWT CONF
TOKEN_LIFETIME_HOURS = os.getenv('TOKEN_LIFETIME_HOURS', 5)

# EMAIL
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)
# EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', True)
