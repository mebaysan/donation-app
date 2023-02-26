#! /bin/bash

python manage.py collectstatic --no-input

python manage.py makemigrations

python manage.py migrate

python manage.py load_countries_states

gunicorn donation.wsgi:application --bind 0.0.0.0:8000