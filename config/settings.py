"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=pv_1g71@nh)o8uyy+o5c@!ia2#85gotasrp)!mm7&!!1gq$ha'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'ab1c-2a03-d000-17-afb8-71ac-4e39-1260-e2cb.ngrok-free.app',
    '127.0.0.1',
    '194.87.79.10'
]
CSRF_TRUSTED_ORIGINS = [
    'https://ab1c-2a03-d000-17-afb8-71ac-4e39-1260-e2cb.ngrok-free.app',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'main',
    'payment_youkassa',

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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
dotenv.load_dotenv()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'USER': os.getenv('POSTGRES_USER'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/user/'

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
ALLOWED_TIME_UNAUTH_USER = 10
SUPPORTED_EXTENSIONS = ['m4a', 'm4b', 'm4p', 'm4r', 'mp3', 'aac', 'ac3', 'wav', 'alac',
                        'flac', 'flv', 'wma', 'amr', 'mpga', 'ogg', 'oga', 'mogg',
                        'svx', 'aif', 'ape', 'au', 'dss', 'opus', 'qcp', 'tta', 'voc', 'wv',
                        'm4p', 'm4v', 'webm', 'mts', 'm2ts', 'ts', 'mov', 'mp2', 'mxf', ]

FILE_UPLOAD_TEMP_DIR = os.path.join(MEDIA_ROOT, 'audio_files/temp')

YOUKASSA_SHOP_ID = os.getenv('YOUKASSA_SHOP_ID')
YOUKASSA_SECRET_KEY = os.getenv('YOUKASSA_SECRET_KEY')
RUB_TO_MINUTE_KOEF = 1 / 3

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
API_HOST_URL = os.getenv('API_HOST_URL')
NATS_SERVER_URL = os.getenv('NATS_SERVER_URL')
QUEUE = os.getenv('QUEUE')

LOG_FILE_PATH = os.path.join(BASE_DIR, 'logs', 'django.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,  # Specify the path to your log file
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('GMAIL_PASS')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_EMAIL_AUTHOR')
DEFAULT_TO_EMAIL = 'almaz28-10@mail.ru'
