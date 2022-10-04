"""
Django settings for twin_dynamics project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend'
)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'organizations',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'accounts',

    'main_app',
    'jsignature',
    'widget_tweaks',
    # 'invitations',
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    'des',
    'sweetify',
    # 'django_nvd3',
    # 'djangobower',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels',
    'storages',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'twin_dynamics.urls'

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

WSGI_APPLICATION = 'twin_dynamics.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'twin_dynamics',
#         'CLIENT': {
#             'host': 'mongodb+srv://twidy_dashboard:fX7AQkxT0zJ4WXhp@cluster0.8obys.mongodb.net/?retryWrites=true&w=majority',
#             'port': 27017,
#         },
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
ASGI_APPLICATION = 'twin_dynamics.routing.application'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('127.0.0.1', 6379),],
#         },
#     },
# }

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    # 'djangobower.finders.BowerFinder',

]

PLOTLY_COMPONENTS = [

    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    'dpd_components'
]
X_FRAME_OPTIONS = 'SAMEORIGIN'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')


# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_DEFAULT_ACL = None
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_IS_GZIPPED = True
# AWS_S3_OBJECT_PARAMETERS = {
# 	'CacheControl': 'max-age=86400',
#
# }
# DEFAULT_FILE_STORAGE = 'twin_dynamics.custom_storage.storages.MediaStorage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ORGS_SLUGFIELD = 'django_extensions.db.fields.AutoSlugField'
# INVITATION_BACKEND = 'main_app.backends.CustomInvitations'
INVITATION_BACKEND = 'organizations.backends.defaults.InvitationBackend'
SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert'

from sweetify.templatetags import sweetify

sweetify.DEFAULT_OPTS = {
    'showConfirmButton': False,
    'timer': 15000,
    'allowOutsideClick': True,
    'confirmButtonText': 'True',
}


EMAIL_BACKEND = 'des.backends.ConfiguredEmailBackend'

# Specifie path to components root (you need to use absolute path)
# BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')
#
# BOWER_PATH = os.path.normpath('C:/Users/MR LAPTOP/AppData/Roaming/npm/bower.cmd')
#
# BOWER_INSTALLED_APPS = (
#     'd3#3.3.13',
#     'nvd3#1.7.1',
# )


#ACCOUNT_ADAPTER = 'education.account_adapter.NoNewUsersAccountAdapter'
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# ACCOUNT_FORMS = {'login': 'main_app.forms.MyCustomSignupForm'}
LOGIN_REDIRECT_URL = '/'
INVITATIONS_SIGNUP_REDIRECT = 'account_signup'
INVITATION_ONLY = True


#DEPLOYMENT SETTING
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
#SECURE_HSTS_SECONDS = 31536000
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True
#SECURE_SSL_REDIRECT = False
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_REFERRER_POLICY = "strict-origin"