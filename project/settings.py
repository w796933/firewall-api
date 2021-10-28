""" Django project settings. """
import ast
import os
import random


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load SETTINGS from a dict literal.
with open(os.path.join(BASE_DIR, 'var', 'settings.py')) as settings_file:
    SETTINGS = ast.literal_eval(settings_file.read())


# Load SECRET_KEY from file or write a new one. Django 2.2.
SECRET_KEY_FILE = os.path.join(BASE_DIR, 'var', 'secret_key')
if os.path.isfile(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE) as secret_fd:
        SECRET_KEY = secret_fd.read().strip()
else:
    SECRET_KEY = ''.join(random.choice(
        'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    ) for _ in range(50))
    with open(SECRET_KEY_FILE, 'w') as secret_fd:
        secret_fd.write(SECRET_KEY)


# Required custom vars

ADMINS = SETTINGS['ADMINS']

SERVER_EMAIL = SETTINGS['SERVER_EMAIL']

TIME_ZONE = SETTINGS['TIME_ZONE']


# Other custom vars

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

DEBUG = False

EMAIL_SUBJECT_PREFIX = '[firewall] '


# Application definition

INSTALLED_APPS = [
    'user.apps.UserConfig',
    'ipset.apps.IpsetConfig',
    'iptables.apps.IptablesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'var', 'db.sqlite3'),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


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

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
