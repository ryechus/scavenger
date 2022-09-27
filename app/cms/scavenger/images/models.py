import logging

from django.conf import settings
from django.db import models
from wagtail.images.models import (AbstractImage, AbstractRendition, Filter,
                                   Image, Rendition)

from scavenger.storage import ImageServiceStorage

logger = logging.getLogger(__name__)


class ImageServiceImageModel(AbstractImage):
    file = models.ImageField(
        upload_to=f"{settings.ENVIRONMENT_NAME}/",
        width_field="width",
        height_field="height",
        storage=ImageServiceStorage,
    )

    admin_form_fields = Image.admin_form_fields

    class Meta:
        managed = False
        db_table = Image.objects.model._meta.db_table

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        renditions = [
            "max-165x165",  # thumbnail gallery in admin
            "fill-640x640",  # main size for home page
            "max-800x600",  # size for image detail page
        ]

        for rendition in renditions:
            self.get_rendition(rendition)

    @property
    def url(self):
        return self.file.url

    def get_rendition(self, filter):
        """
        Returns a ``Rendition`` instance with a ``file`` field value (an
        image) reflecting the supplied ``filter`` value and focal point values
        from this object.
        Note: If using custom image models, an instance of the custom rendition
        model will be returned.
        """
        if isinstance(filter, str):
            filter = Filter(spec=filter)

        cache_key = filter.get_cache_key(self)
        Rendition = self.get_rendition_model()

        try:
            rendition = self.renditions.get(
                filter_spec=filter.spec,
                focal_point_key=cache_key,
            )
        except Rendition.DoesNotExist:
            # Generate the rendition image
            # make GET request to image service
            width = self.width
            height = self.height
            spec = filter.spec.split("-")
            file_url = self.file.name
            if len(spec) == 2:
                width, height = spec[1].split("x")
                file_url += f"?width={width}&height={height}"

            response = self.file.storage.get_url(file_url)
            if str(response.status_code).startswith("4"):
                logger.warning("404 when getting thumbnail")
                return self.renditions.model.objects.last()

            rendition = self.renditions.model(
                width=width,
                height=height,
                image=self,
                filter_spec=filter.spec,
                focal_point_key=cache_key,
            )

            rendition.file.name = response.json().replace(
                f"{settings.IMAGE_SERVICE_CDN}/", ""
            )
            rendition.save()

        return rendition


class CustomRendition(AbstractRendition):
    file = models.ImageField(
        upload_to="images/",
        width_field="width",
        height_field="height",
        storage=ImageServiceStorage,
    )
    image = models.ForeignKey(
        ImageServiceImageModel, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        managed = False
        unique_together = (("image", "filter_spec", "focal_point_key"),)
        db_table = Rendition.objects.model._meta.db_table
