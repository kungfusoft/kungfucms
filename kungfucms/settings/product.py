# PROJECT : kungfucms
# TIME : 2018/11/18 11:21
# AUTHOR : Younger Shen
# EMAIL : youngershen64@gmail.com
# CELL : 13811754531
# WECHAT : 13811754531
import logging
from kungfucms.settings.base import *
from kungfucms.logging.utils import get_log_file

DEBUG = False

INSTALLED_APPS += [
    'kungfucms.apps.system',
    'kungfucms.apps.account',
    'kungfucms.apps.exception'
]

DOMAIN_NAME = env.list('DOMAIN_NAME', default='localhost')

ALLOWED_HOSTS = DOMAIN_NAME

DATABASES = {
    'default': env.db()
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str('CACHE_REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}


AUTH_USER_MODEL = 'account.User'

LOG_LEVEL = env.str('LOG_LEVEL', default='ERROR')

LOG_FORMAT = '%(levelname)s %(asctime)s %(pathname)s %(funcName)s %(lineno)s : %(message)s'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose'
        },
        'file': {
            'level': logging.INFO,
            'class': 'kungfucms.logging.handlers.FileHandler',
            'formatter': 'verbose',
            'filename': get_log_file(),
        },
        'console': {
            'level': logging.DEBUG,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'db': {
            'level': logging.ERROR,
            'class': 'kungfucms.logging.handlers.DBHandler',
        }
    },
    'loggers': {
        'kungfucms': {
            'handlers': ['mail_admins', 'console', 'db', 'file'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'django': {
            'handlers': ['mail_admins', 'console', 'db', 'file'],
            'level': LOG_LEVEL,
            'propagate': False
        }
    }
}
