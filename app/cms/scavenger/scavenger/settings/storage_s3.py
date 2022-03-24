import os

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

AWS_STORAGE_BUCKET_NAME = os.environ.get(
    "AWS_S3_STORAGE_BUCKET", "scavenger-django-storage"
)

AWS_DEFAULT_ACL = "public-read"

MEDIA_ROOT = "/media/"

STATIC_ROOT = "/static/"

STATIC_URL = f'"{os.environ.get("AWS_S3_URL")}"/static/'

MEDIA_URL = f'"{os.environ.get("AWS_S3_URL")}"/media/'
