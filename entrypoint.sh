#!/bin/sh
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ $DEBUG = 1 ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn djangopj.wsgi:application --bind 0.0.0.0:8000
fi
