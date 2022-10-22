#!/bin/sh
poetry run python manage.py makemigrations --noinput
poetry run python manage.py migrate --noinput
poetry run python manage.py collectstatic --noinput

if [ $DEBUG = "True" ]; then
    poetry run python manage.py runserver 0.0.0.0:8000
else
    poetry run gunicorn djangopj.wsgi:application --bind 0.0.0.0:8000
fi
