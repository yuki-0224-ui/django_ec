from .base import *

environ.Env.read_env(env_file=str(BASE_DIR) + "/.env")

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": env.db(),
}

STORAGES = {
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    }
}

INSTALLED_APPS.insert(-1, 'debug_toolbar')
MIDDLEWARE.insert(-1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = ['127.0.0.1', ]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

BASICAUTH_USERS = {
    env('BASIC_AUTH_USER'): env('BASIC_AUTH_PASSWORD')
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
