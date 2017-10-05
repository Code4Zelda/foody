"""
WSGI config for foody project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foody.settings")

application = get_wsgi_application()

#Use whitenoise package to server static files to Heroku.
from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)
