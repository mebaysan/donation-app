# If you want to use this config file, you should set `DEBUG=1` on your terminal

from donation.settings import BASE_DIR

# App Variables to use in templates
APP_NAME = "Donation App"
APP_FAVICON_URL = "https://localhost/favicon.ico"

APP_PAYMENT_RESPONSE_URL = "https://localhost:3000/cart"  # this will be used in payment success and fail urls to redirect user from payment page to cart page

SECRET_KEY = "verySECRETk3y"

ALLOWED_HOSTS = [
    "127.0.0.1:8000",
    "127.0.0.1",
    "localhost",
    "localhost:8000",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

X_FRAME_OPTIONS = "ALLOWALL"

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
    "store_no": "57902",  # 57902 || 496
    "customer_no": "97228291",  # 97228291 || 400235
    "username": "TEPKVT2021",  # TEPKVT2021 || apitest
    "password": "api123",
    "ok_url": "http://127.0.0.1:8000/api/payment-success/",
    "fail_url": "http://127.0.0.1:8000/api/payment-fail/",
    "payment_request_url": "https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelPayGate",
    "payment_approve_url": "https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelProvisionGate",
}
# TEST CARD FOR KUVEYTTURK
# Test Kart Bilgileri
# Kart No: 5188 9619 3919 2544 || 4033 6025 6202 0327
# CVV2: 929 || 861
# Expirydate: 06/25 || 01/30

# JWT CONF
TOKEN_LIFETIME_HOURS = 5

# EMAIL
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "info@baysansoft.com"
EMAIL_HOST_PASSWORD = "bkbkegwqmsfdlsyu"
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
