"""
Django settings for djangoProject project.
Generated by 'django-admin startproject' using Django 3.2.
"""
from pathlib import Path
import os

from dotenv import load_dotenv

# load .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

HASHID_FIELD_SALT = os.environ.get('HASHID_SALT')
HASHID_FIELD_MIN_LENGTH = os.environ.get('HASHID_FIELD_MIN_LENGTH', 7)
HASHID_FIELD_ENABLE_HASHID_OBJECT = os.environ.get('HASHID_FIELD_ENABLE_HASHID_OBJECT', False)
HASHID_FIELD_ENABLE_DESCRIPTOR = os.environ.get('HASHID_FIELD_ENABLE_DESCRIPTOR', False)
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# EMBA stuff
# EMBA location
EMBA_ROOT = '/var/www/emba/'
EMBA_LOG_ROOT = '/var/www/emba_logs'
EMBA_LOG_URL = 'emba_logs/'

# Application definition - defines what apps gets migrated
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',
    'mod_wsgi.server',
    'channels',
    'uploader',
    'users',
    'reporter',
    'dashboard'
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'embark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', EMBA_LOG_ROOT],
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

# CSRF and SESSION cookies are:
# 1. separate for now but basically linked (==CSRF_USE_SESSION)
# 2. only active after login

# CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = False  # False since we will grab it via universal-cookies

SESSION_COOKIE_SAMESITE = 'Strict'
# SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

WSGI_APPLICATION = 'embark.wsgi.application'
ASGI_APPLICATION = 'embark.asgi.application'

# Database - uses *.env to configure
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
        'CONN_MAX_AGE': 300,
        'OPTIONS': {
            # 'threaded': True,
        },
    },
}

# Logging stuff
# ERRORS/WARNINGS->console
# DEBUG->embark.log
# INFO->embark.log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'filename': BASE_DIR / 'debug.log',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': BASE_DIR / 'web.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['info'],
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,  # 10 MiB
            'backupCount': 2,
            'propagate': True,
        },
        'django.requests': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'web': {
            'handlers': ['debug'],
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,  # 10 MiB
            'backupCount': 2,
        },

    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static/'
]
# STATICFILES_STORAGE
# STATICFILES_FINDERS

# URL of Login-Page
LOGIN_URL = ''

# URL of Logout-Page
LOGOUT_REDIRECT_URL = ''

# Upload Media
MEDIA_ROOT = '/var/www/media/'
MEDIA_URL = '/media/'

# Active Firmware
ACTIVE_FW = '/var/www/active/'

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Format string for displaying run time timestamps in the Django admin site. The default
# just adds seconds to the standard Django format, which is useful for displaying the timestamps
# for jobs that are scheduled to run on intervals of less than one minute.
#
# See https://docs.djangoproject.com/en/dev/ref/settings/#datetime-format for format string
# syntax details.
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# Maximum run time allowed for jobs that are triggered manually via the Django admin site, which
# prevents admin site HTTP requests from timing out.
#
# Longer running jobs should probably be handed over to a background task processing library
# that supports multiple background worker processes instead (e.g. Dramatiq, Celery, Django-RQ,
# etc. See: https://djangopackages.org/grids/g/workers-queues-tasks/ for popular options).
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

# redis/channel layers setup
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# SSL stuff
SECURE_HSTS_SECONDS = 0
SECURE_SSL_REDIRECT = False
