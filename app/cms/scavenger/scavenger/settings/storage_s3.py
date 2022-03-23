import os

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_S3_STORAGE_BUCKET")

AWS_DEFAULT_ACL = "public-read"

STATIC_URL = os.environ.get("AWS_S3_URL")

MEDIA_URL = os.environ.get("AWS_S3_URL")
