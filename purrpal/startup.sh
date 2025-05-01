#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn --workers 2 purrpal.wsgi:application --bind 0.0.0.0:8000

