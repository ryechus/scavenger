from django.db import models

# from django.utils.translation import gettext_lazy as _
# from images.storage import ImageServiceStorage
# from wagtail.images.models import AbstractImage, AbstractRendition, Image, get_upload_to


# class CustomImage(AbstractImage):
#     # Add any extra fields to image here
#
#     # eg. To add a caption field:
#     file = models.ImageField(
#         verbose_name=_("file"),
#         upload_to=get_upload_to,
#         width_field="width",
#         height_field="height",
#         storage=ImageServiceStorage,
#     )
#
#     admin_form_fields = Image.admin_form_fields
#
#     class Meta:
#         db_table = "wagtailimages_image"
#         managed = False
#
#
# class CustomRendition(AbstractRendition):
#     image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name="renditions")
#
#     class Meta:
#         unique_together = (("image", "filter_spec", "focal_point_key"),)
#         db_table = "wagtailimages_rendition"
#         managed = False


# class InstagramAccountMedia(models.Model):
#     instagram_account = models.ForeignKey("instagram_sync.InstagramAccount", on_delete=models.CASCADE)
#     image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE)
