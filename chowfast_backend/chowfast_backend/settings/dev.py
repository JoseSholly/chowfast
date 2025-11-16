import os
from datetime import timedelta
from urllib.parse import parse_qsl, urlparse

from chowfast_backend.env import BASE_DIR
from decouple import Csv, config
from dotenv import load_dotenv

from .base import *

load_dotenv()


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
        'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
    }
}


ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

allowed_host_value = config("ALLOWED_HOSTS")

if allowed_host_value:
    ALLOWED_HOSTS.extend(allowed_host_value.split(","))

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

# This production code might break development mode, so we check # This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_COMPRESS = True
    WHITENOISE_MANIFEST_STRICT = True

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000          # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=Csv(),
    default="http://localhost:3000"
)


CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=Csv(),
    default="http://localhost:3000"
)

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
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
    ],
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    
}

# From WSGI
# gunicorn chowfast_backend.wsgi:application --workers 3

# To ASGI (just add this)
# gunicorn chowfast_backend.asgi:application -k uvicorn.workers.UvicornWorker --workers 3