#!/usr/bin/env bash
set -o errexit

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
poetry run python manage.py migrate --noinput || echo "Migration failed, continuing..."

echo "Starting server..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000
