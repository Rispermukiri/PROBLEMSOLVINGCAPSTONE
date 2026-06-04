"""
WSGI config for AttachLink project.
Used by production servers like Gunicorn and uWSGI.
"""

import os
from django.core.wsgi import get_wsgi_application

# Use production settings by default
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attachlink.settings.production')

application = get_wsgi_application()
