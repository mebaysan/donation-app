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
    'username': 'ourusername',
    'password': 'ourpassword',
    'ok_url': 'http://127.0.0.1:8000/transaction-success/',
    'fail_url': 'http://127.0.0.1:8000/transaction-fail/',
    'pos_kart_onay_url': 'https://boatest.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelPayGate',
    'pos_odeme_url': 'https://boatest.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelProvisionGate',
}
