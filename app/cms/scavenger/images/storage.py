import requests
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.core.files.storage import Storage
from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3BotoStorage(ManifestFilesMixin, S3Boto3Storage):  # noqa
    location = "static"


class MediaRootS3BotoStorage(S3Boto3Storage):  # noqa
    location = "media"


class ImageServiceStorage(Storage):
    STORAGE_HOST_NAME = getattr(settings, "IMAGE_SERVICE_STORAGE_HOST_NAME", "http://localhost:8888")

    def delete(self, name):
        ...

    def exists(self, name):
        ...

    def get_accessed_time(self, name):
        ...

    def get_alternative_name(self, file_root, file_ext):
        ...

    def get_available_name(self, name, max_length=None):
        ...

    def get_created_time(self, name):
        ...

    def get_modified_time(self, name):
        ...

    def get_valid_name(self, name):
        return name

    # def generate_filename(self, filename):
    #     ...

    # def listdir(self, path):
    #     ...

    def open(self, name, mode="rb"):
        ...

    # def path(self, name):
    #     ...

    def save(self, name, content, max_length=None):
        response = requests.post(f"{self.STORAGE_HOST_NAME}/upload", files={"file": content})

        return response.json()["url"]

    def size(self, name):
        ...

    def url(self, name):
        ...
