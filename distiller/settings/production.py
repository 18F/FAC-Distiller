"""
Production settings for FAC Distiller.
"""

import json

from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = bool(os.environ.get('DEBUG'))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] "
                      "%(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': "%(levelname)s %(message)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
        'django.template': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    },
}

# In production cloud.gov environments, we expect to find these system
# environment settings variables.
# Include SECRET in the name so if are in DEBUG mode, Django will not include
# these settings in its DEBUG logs.
#VCAP_APPLICATION_SECRET = json.loads(os.environ['VCAP_APPLICATION'])
VCAP_SERVICES_SECRET = json.loads(os.environ['VCAP_SERVICES'])

S3_KEY_DETAILS = VCAP_SERVICES_SECRET['s3'][0]['credentials']
LOAD_TABLE_ROOT = f's3://{S3_KEY_DETAILS["bucket"]}/data-sources'
