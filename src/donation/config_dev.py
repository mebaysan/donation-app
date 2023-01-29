# If you want to use this config file, you should set `DEBUG=True` on your terminal

import os

from donation.settings import BASE_DIR

# App Name to use in templates
APP_NAME = 'Donation App'

SECRET_KEY = "verySECRETk3y"

ALLOWED_HOSTS = []

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
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# KUVEYTTURK CONF
KUVEYTTURK_CONF = {
    'magaza_no': '1234',
    'musteri_no': '1233214',
    'username': 'apitest',
    'password': 'api123',
    'ok_url': 'http://127.0.0.1:8000/api/payment-success/',
    'fail_url': 'http://127.0.0.1:8000/api/payment-fail/',
    'payment_request_url': 'https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelPayGate',
    'payment_approve_url': 'https://boatest.kuveytturk.com.tr/boa.virtualpos.services/Home/ThreeDModelProvisionGate',
}
# TEST CARD FOR KUVEYTTURK
# Test Kart Bilgileri
# Kart No: 4033 6025 6202 0327
# CVV2: 861
# Expirydate: 01/30
