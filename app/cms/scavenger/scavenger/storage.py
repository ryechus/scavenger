import logging

import requests
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from storages.backends.s3boto3 import S3Boto3Storage
from wagtail.images import get_image_model

logger = logging.getLogger(__name__)


class StaticRootS3BotoStorage(ManifestFilesMixin, S3Boto3Storage):  # noqa
    location = "static"


class MediaRootS3BotoStorage(S3Boto3Storage):  # noqa
    location = "media"


@deconstructible
class ImageServiceStorage(Storage):
    def __init__(self, config=None):
        if not config:
            ...
            # option = settings
        ...

    def __eq__(self, other):
        return self == other

    def _open(self, *args, **kwargs):
        return ContentFile(b"", name="this.jpeg")

    def _save(self, name, content):
        response = requests.post(
            f"{settings.IMAGE_SERVICE_HOST}/upload/",
            files={"file": content},
            data={"prefix": get_image_model().file.field.upload_to},
        )
        logger.info(response)
        return response.json()["key"]

    def delete(self, name):
        requests.delete(f"{settings.IMAGE_SERVICE_HOST}/image/{name}")

        return True

    def exists(self, *args, **kwargs):
        ...

    def listdir(self, *args, **kwargs):
        ...

    def size(self, *args, **kwargs):
        ...

    def get_url(self, name):
        return requests.get(f"{settings.IMAGE_SERVICE_HOST}/image/{name}")

    def url(self, name):
        return f"{settings.IMAGE_SERVICE_CDN}/{name}"
