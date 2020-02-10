"""
Base settings for FAC Distiller project.
"""

import os
from pathlib import Path

import dj_database_url


BASE_DIR = Path(__file__).parents[1]
PROJECT_ROOT = BASE_DIR.parents[0]

# Set this to the root path for downloading and loading tables to ETL
# On local dev, this may be a filesystem path.
# In production, it may be an S3 url (s3://...)
LOAD_TABLE_ROOT = None

# Set this to the path to save FAC documents to.
# On local dev, this may be a filesystem path.
# In production, it may be an S3 url (s3://...)
FAC_DOCUMENT_DIR = None

# Set this to the root path of FAC crawl logs (CSVs).
# On local dev, this may be a filesystem path.
# In production, it may be an S3 url (s3://...)
FAC_CRAWL_ROOT = None

# Set this to a dict of the form:
# {'access_key_id': 'XX',
#  'secret_access_key': 'XXX',
#  'region': 'us-gov-west-1',
#  'bucket': 'XX'}
S3_KEY_DETAILS = None

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.cloud.gov',
]

SECRET_KEY = 'SECRET'

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',

    'django_apscheduler',
    'fontawesome_free',
    'localflavor',
    'widget_tweaks',

    'distiller.audit_search.apps.AuditSearchConfig',
    'distiller.data.apps.DataConfig',
    'distiller.fac_scraper.apps.FacScraperConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'distiller.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'distiller.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    '/var/www/static/',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATABASES = {
    'default': dj_database_url.config(default='postgres://postgres:postgres@127.0.0.1/distiller')
}

CHROME_DRIVER_LOCATION = os.path.join('/usr/local/bin/chromedriver')
