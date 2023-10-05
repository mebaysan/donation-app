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
mv src/.env.dev src/.env # create .env file
make install # install the requirements
make create-devdb # create project dev db (you have to have Docker on your machine)
make migration # create the db
make load_countries_states # load country and state_provinces data
make superuser # create a super user 
make runserver # run the project
```

## Test Project

```bash
make install # install the requirements
make test # run the tests
```

# Environment Variables

You can check [`.env.example`](./src/.env.dev) file to see the environment variables.