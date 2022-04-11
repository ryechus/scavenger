import os

DEFAULT_FILE_STORAGE = "scavenger.storage.MediaRootS3BotoStorage"

STATICFILES_STORAGE = "scavenger.storage.StaticRootS3BotoStorage"

AWS_STORAGE_BUCKET_NAME = os.environ.get(
    "AWS_S3_STORAGE_BUCKET", "scavenger-django-storage"
)

AWS_LOCATION = os.environ.get("env", "")

AWS_DEFAULT_ACL = "public-read"

MEDIA_ROOT = "/media/"

STATIC_ROOT = "/static/"

STATIC_URL = f'{os.environ.get("AWS_S3_URL")}/static/'

MEDIA_URL = f'{os.environ.get("AWS_S3_URL")}/media/'

AWS_QUERYSTRING_AUTH = False
