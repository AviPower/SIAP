"""
Django settings for SIAP project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fa(+o%tw(m8rtoggy4-f5odj%a7m2tv178bn+3$+_!$nn495ye'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.core.urlresolvers import reverse_lazy

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('listar_proyectos')
LOGOUT_URL = reverse_lazy('logout')
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.inicio',
    'apps.usuarios',
    'apps.proyectos',
    'apps.roles',
    'apps.fases',
    'apps.tiposDeItem',
    'apps.items', 
    'apps.lineaBase',
    'apps.solicitudes',
    'apps.reportes'
)

DELETE_MESSAGE = 50

MESSAGE_TAGS = {
    DELETE_MESSAGE : 'deleted',
}


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'SIAP.urls'

WSGI_APPLICATION = 'SIAP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bd_siap',
        'USER': 'adminbd',
        'PASSWORD': '2014is2',
        'HOST': 'localhost',
        'PORT': '5432',
        },
    'produ': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'bd_siap_des',
         'USER': 'adminbd',
         'PASSWORD': '2014is2',
         'HOST': 'localhost',
         'PORT': '5432',
    }
}



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-PY'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#MEDIA_URL = '/media/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

MEDIA_URL = 'http://siap.com/var/www/'
MEDIA_ROOT = '/var/www/'
#MEDIA_ROOT = '/tmp/'
#MEDIA_ROOT = '/home/alvarenga/PycharmProjects/SIAP/media/'

EMAIL_HOST_USER = 'gestionsiap@gmail.com'

EMAIL_HOST_PASSWORD = 'sistemainformatico'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587
EMAIL_USE_TLS = True