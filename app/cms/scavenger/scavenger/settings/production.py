import os  # noqa

from .base import *  # noqa
from .storage_s3 import *  # noqa
from .sentry import *  # noqa

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["https://scavenger.news"]
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
    }
}
