from pathlib import Path

from P4SBonjour import bonjour_app
import os


BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5&-!-o#$p$u2oa#1ga$4*a1v*rt$=79k63(@efruh0-iwob6sw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'P4SBonjour.accounts',
    'P4SBonjour.bonjour_app',
    'dbbackup'
]

SESSION_COOKIE_AGE = 43200

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_NAME = 'sessionID'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'P4SBonjour.accounts.middleware.LoginDelayMiddleware',
    'P4SBonjour.accounts.middleware.LoginLockoutMiddleware',
    'P4SBonjour.accounts.middleware.MFAMiddleware',
]

ROOT_URLCONF = 'P4SBonjour.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'P4SBonjour.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'inventory.db'),
    }
}


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

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'P4SBonjour/backup')}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{asctime} [{levelname}] {name}:{lineno} {message}',
            'style': '{',
        },
        'json': {
            'format': '{{"time": "{asctime}", "level": "{levelname}", "name": "{name}", "lineno": {lineno}, '
                      '"message": "{message}"}}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'P4SBonjour/logs', 'django_debug.log'),
            'maxBytes': 1024*1024*5,  # 5MB
            'backupCount': 7,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.google.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bonjouremailserver@gmail.com'
EMAIL_HOST_PASSWORD = 'BonjourApplicationAccess'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'

MAX_LOGIN_ATTEMPTS = 1
LOGIN_TIMEOUT = 300
