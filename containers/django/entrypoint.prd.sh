#!/bin/sh
set -eu

mkdir -p ${APP_ROOT}/tmp/gunicorn_sockets

# Execute migration
poetry run python manage.py migrate

# Run Django application
poetry run gunicorn project.wsgi:application --bind=unix://${APP_ROOT}/tmp/gunicorn_socket

exec "$@"