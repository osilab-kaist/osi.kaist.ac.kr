"""
Django settings for osilab_homepage project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

import environ

print("Loading settings.py...", file=sys.stderr)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read environment variables from .env file (optional)
env = environ.Env(
    DEBUG=(bool, None),
    STATIC_ROOT=(str, None),
    MEDIA_ROOT=(str, None),
    SECRET_KEY=(str, None),
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Project paths
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if env("SECRET_KEY") is not None:
    SECRET_KEY = env("SECRET_KEY")
    print("Using custom SECRET_KEY", file=sys.stderr)
else:
    SECRET_KEY = '7u3e$ei+h9*w@m&k2nkd9i0$m^pzf!mitcu=_9qn%a602wfk)w'
    print(f"Using default SECRET_KEY: {SECRET_KEY}", file=sys.stderr)

# SECURITY WARNING: don't run with debug turned on in production!
if env("DEBUG") is not None:
    DEBUG = env("DEBUG")
    print(f"Using custom DEBUG: {DEBUG}", file=sys.stderr)
else:
    DEBUG = True
    print(f"Using default DEBUG: {DEBUG}", file=sys.stderr)

ALLOWED_HOSTS = ["osi.kaist.ac.kr", "localhost", "127.0.0.1", "143.248.92.48", "*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap5',
    'django_summernote',
    'core',
    'django_extensions',
]

NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.HideServerMiddleware',
]

ROOT_URLCONF = 'osilab_homepage.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
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

WSGI_APPLICATION = 'osilab_homepage.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'core.User'
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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'
if env("STATIC_ROOT") is not None:
    STATIC_ROOT = env("STATIC_ROOT")
    print(f"Using custom STATIC_ROOT: {STATIC_ROOT}", file=sys.stderr)

if env("MEDIA_ROOT") is not None:
    MEDIA_ROOT = env("MEDIA_ROOT")
    print(f"Using custom MEDIA_ROOT: {MEDIA_ROOT}", file=sys.stderr)
else:
    MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
    print(f"Using default MEDIA_ROOT: {MEDIA_ROOT}", file=sys.stderr)
MEDIA_URL = '/media/'

SUMMERNOTE_THEME = 'bs4'

SUMMERNOTE_CONFIG = {
    'summernote': {
        # Change editor size
        'width': '100%',
        'height': '480',

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            # ['fontname', ['fontname']],
            # ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            # ['insert', ['link', 'picture', 'video']],
            ['insert', ['link']],
            # ['view', ['fullscreen', 'codeview', 'help']],
            ['view', ['codeview', 'help']],
        ],
        'styleTags': ['p', 'h1', 'h2', 'quote', 'code'],

        'popover': {
        },

        # Or, explicitly set language/locale for editor
        'lang': 'ko-KR',
    },

    # 'disable_attachment': True
}

print("Done loading settings.py", file=sys.stderr)
