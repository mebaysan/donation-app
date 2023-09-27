[![CI - Image Deploy To Docker Hub](https://github.com/mebaysan/donation-app/actions/workflows/ci.yaml/badge.svg)](https://github.com/mebaysan/donation-app/actions/workflows/ci.yaml)[![CI - Develop Branch Test](https://github.com/mebaysan/donation-app/actions/workflows/ci-develop.yaml/badge.svg)](https://github.com/mebaysan/donation-app/actions/workflows/ci-develop.yaml)

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Core Django Settings](#core-django-settings)
- [For Development](#for-development)
- [Backup](#backup)
- [Codebase Related Topic](#codebase-related-topic)
  - [Static \& Media Files for Production](#static--media-files-for-production)
  - [Custom Authentication Backend](#custom-authentication-backend)
- [Development Environment](#development-environment)
  - [Run Project](#run-project)
- [Environment Variables](#environment-variables)


# Core Django Settings

I seperate the prod and dev environments. [config_prod.py](./settings/config_prod.py) file is being used for prod
environments and [config_prod.py](./settings/config_dev.py) for dev environments. We need to implement the lines
in [settings.py](./settings/settings.py) file to use these seperated environments.

# For Development

You can use [dev-postgres.sh](scripts/dev-postgres.sh) to create a development database.


# Backup

You can use [backuper-db.sh](scripts/backuper-db.sh) to backup your database inside Docker container.

You can use [backuper-web.sh](scripts/backuper-web.sh) to backup your django data inside Docker container.

You can create a crontab by using the command below.

```
sudo crontab -e
```

# Codebase Related Topic

## Static & Media Files for Production

```bash
STATIC_URL = "/django-static/" # for proxy purposes

MEDIA_URL = "/django-media/" # for proxy purposes
```

## Custom Authentication Backend

For this app's purpose, we can be logged in via username or phone_number. Application
uses [`apps.management.authentication.JWTAuthentication`](./src/apps/management/authentication.py) class for rest
framework views.

To obtain a token, we use `/api/token/` endpoint. It uses [`ObtainTokenView`](./src/apps/management/api/views.py) view.

# Development Environment

## Run Project

To override the config variables, you can update the variables in [`config_dev.py`](./src/donation/config_dev.py) file.

```bash
export DEBUG=1 # to use the dev conf
make create-devdb # create project dev db (you have to have Docker on your machine)
make migration # create the db
make load_countries_states # load country and state_provinces data
make superuser # create a super user 
make runserver # run the project
```

# Environment Variables

```bash
# App Variables to use in templates
APP_NAME=My Donation App
APP_FAVICON_URL=xyz.com/favicon.png

APP_PAYMENT_RESPONSE_URL=https://domain.com/cart # this will be used in payment success and fail urls to redirect user from payment page to cart page

SECRET_KEY=secret

ALLOWED_HOSTS=HOST_1 HOST_2

CORS_ALLOWED_ORIGINS=ORIGIN_1 ORIGIN_2

CSRF_TRUSTED_ORIGINS=ORIGIN_1 ORIGIN_2

X_FRAME_OPTIONS=SAMEORIGIN # DENY ALLOWALL SAMEORIGIN

SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

DB_NAME=somedb
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=myuser
DB_PASSWORD=myuser_password

# KUVEYTTURK CONF
KUVEYTTURK_STORE_NO=57902 # Test Creds from KuveytTurk
KUVEYTTURK_CUSTOMER_NO=97228291 # Test Creds from KuveytTurk
KUVEYTTURK_USERNAME=TEPKVT2021 # Test Creds from KuveytTurk
KUVEYTTURK_PASSWORD=api123 # Test Creds from KuveytTurk
KUVEYTTURK_OK_URL=https://<YOUR_HOST>/api/payment-success/
KUVEYTTURK_FAIL_URL=https://<YOUR_HOST>/api/payment-fail/
KUVEYTTURK_PAYMENT_REQUEST_URL=https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelPayGate
KUVEYTTURK_PAYMENT_APPROVE_URL=https://sanalpos.kuveytturk.com.tr/ServiceGateWay/Home/ThreeDModelProvisionGate

# JWT CONF
TOKEN_LIFETIME_HOURS=5

# EMAIL
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=yourmail@gmail.com
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```