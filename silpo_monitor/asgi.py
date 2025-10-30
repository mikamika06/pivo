"""
ASGI config for silpo_monitor project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silpo_monitor.settings")

application = get_asgi_application()

