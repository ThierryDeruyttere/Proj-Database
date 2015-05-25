"""
Django settings for CodeGalaxy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import pymysql
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

pymysql.install_as_MySQLdb()

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'codegalaxy/templates'),
                 os.path.join(BASE_DIR, 'codegalaxy/exercises/templates'),
                 os.path.join(BASE_DIR, 'codegalaxy/evaluation/templates'),
                 os.path.join(BASE_DIR, 'codegalaxy/challenges/templates')]
STATICFILES_DIRS = (os.path.join(BASE_DIR, "codegalaxy/static"),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x(zzx)fo0fj05n*)%uqk(pp!fz$i!79ihyt-n%o68dcw1u3ee-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'foundation',
    'dbw',
    'chartjs',
    'custom_filters',

)

TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'codegalaxy.urls'

WSGI_APPLICATION = 'codegalaxy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codegalaxy',
        'USER': 'root',
        'PASSWORD': 'ruien9690',
        'HOST': 'localhost'
    },
    'sandbox': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sandbox',
        'USER': 'sandbox',
        'PASSWORD': 'sandbox',
        'HOST': 'localhost'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
