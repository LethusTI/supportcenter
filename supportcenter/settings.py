# -*- coding: utf-8 -*-

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRODUCTION = False
# Indica se estamos rodando a versão de produção ou desenvolvimento
value = os.environ.get('PRODUCTION')
if value:
    PRODUCTION = value == 'true'
    
DEBUG = not PRODUCTION
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Lethus', 'suporte@lethus.com.br'),
)

DEPLOY_URL = 'http://supportcenter.lethussaude.com.br'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'no-reply@lethus.com.br'
DEFAULT_FROM_EMAIL = 'no-reply@lethus.com.br'
EMAIL_HOST_PASSWORD = 'Lethus725'
EMAIL_PORT = 587

MANAGERS = ADMINS

if PRODUCTION:
    MONGODB_DATABASE = 'supportcenter'
else:
    MONGODB_DATABASE = 'supportcenterdev'
    
MONGODB_HOST = 'localhost'
MONGODB_USERNAME = None
MONGODB_PASSWORD = None

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'fake.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt_BR'
LANGUAGES = (('pt_BR', u"Português"),)

USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y - H:i:s'

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

if PRODUCTION:
    STATIC_URL = 'http://static.lethussaude.com.br/sp/'
else:
    STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'e!btm%*mxur9*c9nhw_^wh8d=^_w^c8(ih7dz2r158-a+(dkj='

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "supportcenter.common.context_processors.distribuitor",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'supportcenter.accounts.auth.MongoEngineBackend',
)

SESSION_ENGINE = 'mongoengine.django.sessions'

ROOT_URLCONF = 'supportcenter.urls'
WSGI_APPLICATION = 'supportcenter.wsgi.application'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'lethusbox',
    
    'supportcenter.common',
    'supportcenter.accounts',
    'supportcenter.faq',
    'supportcenter.forum',
    'supportcenter.contact',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from django.contrib import messages

MESSAGE_TAGS = {
    messages.DEBUG: '',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: '',
    messages.ERROR: 'alert-error',}
