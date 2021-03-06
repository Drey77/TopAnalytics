"""
Django settings for TopAnalytics project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2t*3sj3wkwj0eztbr^37tg3$oiv7vw)dcg38vu*w%5rn69c3ak'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.211.128', 'localhost', '127.0.0.1', 'andre.test.topchretien.com', 'www.andre.test.topchretien.com', 'testserver']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_extensions',
    'leaflet',
    'djgeojson',

    # general
    'topanalytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_URL = '/login/'
ROOT_URLCONF = 'topanalytics.urls'

MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, '..', 'media'))
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, './templates')],
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

WSGI_APPLICATION = 'topanalytics.wsgi.application'

# GeoIP Path :
GEOIP2_DATABASE_PATH = 'topanalytics/geoip/GeoIP2-City.mmdb'
# Path to the GeoIP2 city database. If none, no geolocalisation will be done.
# GEOIP2_DATABASE_PATH = os.environ.get('topanalytics/geoip/', None)
#os.path.join(BASE_DIR, 'topanalytics/geoip')

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'topanalytics',
        # 'USER': '',
        # 'PASSWORD': '',
        # 'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        # 'PORT': os.environ.get('DATABASE_PORT', 5432),
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'topanalytics',
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', 5432),
        'USER': '',
        'PASSWORD': ''
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

LEAFLET_CONFIG = {
    'DEFAULT_CENTER':(48.859, 2.342),
    'DEFAULT_ZOOM': 4,
    'MIN_ZOOM': 2,
    'MAX_ZOOM': 18,
    'MINIMAP': True,
}