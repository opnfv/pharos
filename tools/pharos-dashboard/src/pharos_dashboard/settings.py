import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ['DEBUG']

# Application definition

INSTALLED_APPS = [
    'dashboard',
    'booking',
    'account',
    'jenkins',
    'notification',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap3',
    'crispy_forms',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'pharos_dashboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'pharos_dashboard.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LOGIN_REDIRECT_URL = '/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

BOOTSTRAP3 = {
    'set_placeholder': False,
}

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    }
}


# Rest API Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

MEDIA_ROOT = '/media'
STATIC_ROOT = '/static'

# Jira Settings
CREATE_JIRA_TICKET = False

JIRA_URL = os.environ['JIRA_URL']

JIRA_USER_NAME = os.environ['JIRA_USER_NAME']
JIRA_USER_PASSWORD = os.environ['JIRA_USER_PASSWORD']

OAUTH_CONSUMER_KEY = os.environ['OAUTH_CONSUMER_KEY']
OAUTH_CONSUMER_SECRET = os.environ['OAUTH_CONSUMER_SECRET']

OAUTH_REQUEST_TOKEN_URL = JIRA_URL + '/plugins/servlet/oauth/request-token'
OAUTH_ACCESS_TOKEN_URL = JIRA_URL + '/plugins/servlet/oauth/access-token'
OAUTH_AUTHORIZE_URL = JIRA_URL + '/plugins/servlet/oauth/authorize'

OAUTH_CALLBACK_URL = JIRA_URL + '/accounts/authenticated'

# Celery Settings
CELERY_TIMEZONE = 'UTC'

RABBITMQ_URL = 'rabbitmq'
BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'

CELERYBEAT_SCHEDULE = {
    'sync-jenkins': {
        'task': 'jenkins.tasks.sync_jenkins',
        'schedule': timedelta(minutes=5)
    },
    'send-booking-notifications': {
        'task': 'notification.tasks.send_booking_notifications',
        'schedule': timedelta(minutes=5)
    },
    'clean-database': {
        'task': 'dashboard.tasks.database_cleanup',
        'schedule': timedelta(hours=24)
    },
}