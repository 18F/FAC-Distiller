"""
Default settings for a development environment.

If `DJANGO_SETTINGS_MODULE` is not defined, and `distiller.settings.local` does
not exist, these settings will be loaded by default.
"""

from .base import *

DEBUG = True

SECRET_KEY = 'SECRET'
