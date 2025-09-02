"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# for migrate
from django.core.management import call_command
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# for migrate
django.setup()
try:
    call_command("migrate", interactive=False)
except Exception as e:
    print("⚠️ Auto-migrate failed:", e)

application = get_wsgi_application()
