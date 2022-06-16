from django.contrib.staticfiles.storage import ManifestFilesMixin
from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3BotoStorage(ManifestFilesMixin, S3Boto3Storage):  # noqa
    location = "static"


class MediaRootS3BotoStorage(ManifestFilesMixin, S3Boto3Storage):  # noqa
    location = "media"
