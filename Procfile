web: gunicorn config.wsgi:application
celery: celery -A config worker -l info
celery-beat: celery -A config beat -l info
