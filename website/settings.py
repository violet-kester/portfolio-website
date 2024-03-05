from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'portfolio-website-dx2t.onrender.com',
    'violetkester.com'
]


# Application definition -------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_htmx',
    'taggit',
    'core',
    'projects',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
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


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Enable logging
# https://docs.djangoproject.com/en/5.0/topics/logging/#examples

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}


# Media files (uploaded photos and other media) --------------------------

# Base URL for media files

MEDIA_URL = ''

# Base directory for media files
# NOTE: Not necessary when serving media files from S3

# MEDIA_ROOT = BASE_DIR / 'media/'


# Static files (CSS, JavaScript, logos, etc.) ----------------------------

# Base URL for static files

STATIC_URL = 'static/'

# Add top-level `static/` directory to static files directories list

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# (Production) Where to collect static files used in production

STATIC_ROOT = BASE_DIR / "staticfiles"

# (Production) Enable AWS S3 and WhiteNoise storage backends
# https://whitenoise.readthedocs.io/en/stable/django.html
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.environ.get('AWS_STORAGE_BUCKET_NAME'),
            "region_name": os.environ.get('AWS_S3_REGION_NAME'),
            "access_key": os.environ.get('AWS_ACCESS_KEY_ID'),
            "secret_key": os.environ.get('AWS_SECRET_ACCESS_KEY'),
            "custom_domain": os.environ.get('AWS_S3_CUSTOM_DOMAIN'),
            "cloudfront_key_id": os.environ.get('AWS_CLOUDFRONT_KEY_ID'),
            "cloudfront_key": os.environ.get('AWS_CLOUDFRONT_KEY'),
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Email server configuration ---------------------------------------------

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'kester.violet.j@gmail.com'

EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')

EMAIL_PORT = 587

EMAIL_USE_TLS = True
