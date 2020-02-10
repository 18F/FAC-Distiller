"""
Default settings for a development environment.

If `DJANGO_SETTINGS_MODULE` is not defined, and `distiller.settings.local` does
not exist, these settings will be loaded by default.
"""

from .base import *

DEBUG = True

SECRET_KEY = 'SECRET'

LOAD_TABLE_ROOT = str(PROJECT_ROOT / 'imports')
FAC_DOCUMENT_DIR = PROJECT_ROOT / 'fac-documents'
FAC_CRAWL_ROOT = PROJECT_ROOT / 'fac-crawls'
