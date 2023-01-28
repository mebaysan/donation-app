# Values are coming from docker-compose.yml
import os

from donation.settings import BASE_DIR

# App Name to use in templates
APP_NAME = os.getenv("APP_NAME")

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

# AWS Credentials
AWS_ACCESS_KEY_ID = 'your_access_key'
AWS_SECRET_ACCESS_KEY = 'your_secret_key'
AWS_STORAGE_BUCKET_NAME = 'your_bucket_name'
AWS_S3_REGION_NAME = 'your_region_name'

# APP MEDIA STORAGE TYPE
APP_MEDIA_STORAGE_TYPE = os.getenv("APP_MEDIA_STORAGE_TYPE")  # set 'S3' to use S3

if APP_MEDIA_STORAGE_TYPE == 'S3':
    # To store files in S3
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # Media root for prod mode. You should use 3rd party storage for these
    MEDIA_ROOT = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/media/'
else:
    MEDIA_ROOT = BASE_DIR / 'media'

# KUVEYTTURK CONF
KUVEYTTURK_CONF = {
    'magaza_no': os.getenv('KUVEYTTURK_MAGAZA_NO'),
    'musteri_no': os.getenv('KUVEYTTURK_MUSTERI_NO'),
    'username': os.getenv('KUVEYTTURK_USERNAME'),
    'password': os.getenv('KUVEYTTURK_PASSWORD'),
    'ok_url': os.getenv('KUVEYTTURK_OK_URL'),
    'fail_url': os.getenv('KUVEYTTURK_FAIL_URL'),
    'payment_request_url': 'https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelPayGate',
    'payment_approve_url': 'https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelProvisionGate',
}
