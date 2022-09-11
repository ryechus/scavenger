from django.db import models
from scavenger.storage import ImageServiceStorage
from wagtail.images.models import (AbstractImage, AbstractRendition, Image,
                                   Rendition)


class ImageServiceImageModel(AbstractImage):
    file = models.ImageField(
        upload_to="",
        width_field="width",
        height_field="height",
        storage=ImageServiceStorage,
    )

    admin_form_fields = Image.admin_form_fields

    class Meta:
        managed = False
        db_table = Image.objects.model._meta.db_table

    def get_rendition(self, filter):
        """
        Returns a ``Rendition`` instance with a ``file`` field value (an
        image) reflecting the supplied ``filter`` value and focal point values
        from this object.
        Note: If using custom image models, an instance of the custom rendition
        model will be returned.
        """
        if self.renditions.last() is not None:
            print("has renditions")

            return self.renditions.last()

        return Rendition.objects.last()


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        ImageServiceImageModel, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        managed = False
        unique_together = (("image", "filter_spec", "focal_point_key"),)
        db_table = Rendition.objects.model._meta.db_table
