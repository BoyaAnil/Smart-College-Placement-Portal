import os

from django.core.wsgi import get_wsgi_application

# Vercel Python runtime expects an `app` variable for WSGI/ASGI entrypoints.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "placement_portal.settings")
app = get_wsgi_application()
