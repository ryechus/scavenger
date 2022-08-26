import base64
import logging

from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel

logger = logging.getLogger("")


class Post(Page):
    artists = ClusterTaggableManager(
        through="artists.PostArtist", blank=True, verbose_name="artist", related_name="artist_posts"
    )
    tags = ClusterTaggableManager(through="artists.PostTag", blank=True)
    uuid = models.UUIDField(null=True, unique=True)

    content_panels = Page.content_panels + [
        InlinePanel("post_images", label="Post images"),
        FieldPanel("artists", heading="artists"),
        FieldPanel("tags"),
    ]
    settings_panels = [FieldPanel("first_published_at", heading="Publish date")] + Page.settings_panels
    context_object_name = "post"

    class Meta:
        ordering = ("-first_published_at",)

    @property
    def images(self):
        return self.post_images


class RichPost(Post):
    body = RichTextField(blank=True)  # this field is being removed

    content_panels = Post.content_panels + [
        FieldPanel("body"),
    ]


class PostImages(Orderable):
    """Image model that allows ordering images on posts"""

    post = ParentalKey(Post, on_delete=models.CASCADE, related_name="post_images")
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.PROTECT, related_name="post_images")
    # can be used to display images using base64
    base64_bin = models.BinaryField(null=True)
    # location_data
    panels = [ImageChooserPanel("image")]

    def save(self, *args, **kwargs):
        logger.info(f"base64 encoding image {self.image}")
        self.base64_bin = base64.b64encode(self.image.file.read())
        super().save(*args, **kwargs)
