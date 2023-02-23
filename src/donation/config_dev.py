# If you want to use this config file, you should set `DEBUG=1` on your terminal

from donation.settings import BASE_DIR

# App Variables to use in templates
APP_NAME = "Donation App"
APP_FAVICON_URL = "https://ihyavakfi.org.tr/media/site/favicon.png"

SECRET_KEY = "verySECRETk3y"

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "USER": "postgres",
        "PASSWORD": "mysecretpassword",
    }
}

# Media root for dev mode
MEDIA_ROOT = BASE_DIR / "media"

# KUVEYTTURK CONF
KUVEYTTURK_CONF = {
    "store_no": "57902",
    "customer_no": "97228291",
    "username": "TEPKVT2021",
    "password": "api123",
    "ok_url": "http://127.0.0.1:8000/api/payment-success/",
    "fail_url": "http://127.0.0.1:8000/api/payment-fail/",
    "payment_request_url": "https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelPayGate",
    "payment_approve_url": "https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelProvisionGate",
}
# TEST CARD FOR KUVEYTTURK
# Test Kart Bilgileri
# Kart No: 5188 9619 3919 2544
# CVV2: 929
# Expirydate: 06/25

# JWT CONF
TOKEN_LIFETIME_HOURS = 5

# EMAIL
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "info@baysansoft.com"
EMAIL_HOST_PASSWORD = "bkbkegwqmsfdlsyu"
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
