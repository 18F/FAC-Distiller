from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG is currently only turned on in dev settings, but better safe than sorry.
DEBUG = True  # Revisit whether runserver is incompatible with collectstatic

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
