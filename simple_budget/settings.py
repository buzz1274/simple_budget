"""
Django settings for simple_budget project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
...
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import yaml
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l05&x3tvwwn(d%tgmb_mf36+rrhe8qo-d@e9ar_xiw&_ab)0gu'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_budget',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "simple_budget.context_processors.quicken_import_active",
    "simple_budget.context_processors.get_message",
    "simple_budget.context_processors.unassigned_transaction_categories",
)

TEMPLATE_DIRS = (
    BASE_DIR + '/budget/templates/',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

ROOT_URLCONF = 'simple_budget.urls'

WSGI_APPLICATION = 'simple_budget.wsgi.application'

with open(BASE_DIR + '/simple_budget/config.yaml') as f:
    config = yaml.load(f)

    if 'server_type' in config and config['server_type'] == 'LIVE':
        DB_HOST = os.environ['POSTGRES_PORT_5432_TCP_ADDR']
        TEMPLATE_DEBUG = False
        DEBUG = False
    else:
        DB_HOST = os.environ['POSTGRES_PORT_5432_TCP_ADDR']
        TEMPLATE_DEBUG = True
        DEBUG = True

    if 'python_path' in config:
        PYTHON_PATH = config['python_path']
    else:
        PYTHON_PATH = None

    if 'backup_path' in config:
        BACKUP_PATH = config['backup_path']
    else:
        BACKUP_PATH = None

    if 'backup_files_to_keep' in config:
        BACKUP_FILES_TO_KEEP = config['backup_files_to_keep']
    else:
        BACKUP_FILES_TO_KEEP = None

    if 'start_date' in config:
        START_DATE = config['start_date']
    else:
        START_DATE = None

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'accounts',
        'USER': 'accounts',
        'HOST': DB_HOST,
        'PORT': 5432,
        'PASSWORD': 'accounts'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LOGIN_URL = '/login'
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
TEMP_SAVE_PATH = '/tmp/'
QUICKEN_IMPORT_ACTIVE = True
SESSION_SAVE_EVERY_REQUEST = True

