import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa

sentry_sdk.init(
    dsn="https://467ebc746f1d4f0ab6c2fdcdc6fb93de@o925654.ingest.sentry.io/6267343",
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

ALLOWED_HOSTS = ["scavenger.news"]
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
