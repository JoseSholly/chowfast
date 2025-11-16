import os
from datetime import timedelta

from chowfast_backend.env import BASE_DIR
from decouple import config
from dotenv import load_dotenv

from .base import *

load_dotenv()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRESQL_DB_NAME"),
        "USER": config("POSTGRESQL_DB_USER"),
        "PASSWORD": config("POSTGRESQL_DB_PASSWORD"),
        "HOST": config("POSTGRESQL_DB_HOST"),
        "PORT": config("POSTGRESQL_DB_PORT"),
        "CONN_MAX_AGE": 600,
    }
}


ALLOWED_HOSTS = []

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


SIMPLE_JWT = {
    # How long the access token is valid (e.g., 5 minutes, 1 hour)
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3), 
    
    # How long the refresh token is valid (e.g., 1 day, 30 days)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    
    # Other security settings
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config("SECRET_KEY"), # Uses your Django secret key
    'AUTH_HEADER_TYPES': ('Bearer',), # Standard header type
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",  # Default permission
    ),

    
    # Define how data is returned (JSON is the default)
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer', # Great for development
    ],
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    
}