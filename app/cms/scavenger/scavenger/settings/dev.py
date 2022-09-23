from .base import *  # noqa
from .cache import *  # noqa
from .hosts import *  # noqa
from .sentry import *  # noqa
from .storage_s3 import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# INSTALLED_APPS += ["elasticapm.contrib.django"]

# ELASTIC_APM = {
#     # Set the required service name. Allowed characters:
#     # a-z, A-Z, 0-9, -, _, and space
#     "SERVICE_NAME": "scavenger-cms",
#     # Use if APM Server requires a secret token
#     "SECRET_TOKEN": os.environ.get("ELASTIC_APM_SECRET"),
#     # Set the custom APM Server URL (default: http://localhost:8200)
#     "SERVER_URL": os.environ.get("ELASTIC_APM_SERVER_URL"),
#     # Set the service environment
#     "ENVIRONMENT": os.environ.get("ENVIRONMENT"),
# }

MIDDLEWARE = [
    "allow_cidr.middleware.AllowCIDRMiddleware",
    # "elasticapm.contrib.django.middleware.TracingMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
] + MIDDLEWARE

CACHE_MIDDLEWARE_SECONDS = 45

# As far as I can tell this is the default subnet cidr for kubernetes default namespace
ALLOWED_CIDR_NETS = ["10.244.0.0/16"]

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
        "level": "INFO",
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

FIELD_ENCRYPTION_KEY = os.environ["FIELD_ENCRYPTION_KEY"]

GRAPH_API_REDIRECT_URI = "https://scavenger.news"

GRAPH_API_APP_ID = 445208100863812

IMAGE_SERVICE_HOST = "https://images.scavenger.news"
