import requests
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from storages.backends.s3boto3 import S3Boto3Storage


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
            "https://images.scavenger.news/upload/",
            files={"file": content},
            data={"key": name},
        )
        print(vars(response))
        return name

    def delete(self, *args, **kwargs):
        ...

    def exists(self, *args, **kwargs):
        ...

    def listdir(self, *args, **kwargs):
        ...

    def size(self, *args, **kwargs):
        ...

    def url(self, name):
        return requests.get(f"https://images.scavenger.news/image/{name}")
