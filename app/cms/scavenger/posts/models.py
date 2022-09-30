import base64
import logging

from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from rest_framework import serializers
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images import get_image_model_string
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailvideos.edit_handlers import VideoChooserPanel

logger = logging.getLogger("")


class PostImages(Orderable):
    """Image model that allows ordering images on posts"""

    post = ParentalKey(
        "posts.Post", on_delete=models.CASCADE, related_name="post_images"
    )
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.PROTECT,
        related_name="post_images",
        null=True,
        blank=True,
    )
    image_new = models.ForeignKey(
        "images.ImageServiceImageModel",
        on_delete=models.PROTECT,
        related_name="post_images_new",
        null=True,
        blank=True,
    )
    video = models.ForeignKey(
        "wagtailvideos.Video",
        on_delete=models.PROTECT,
        related_name="video_posts",
        null=True,
        blank=True,
    )
    # can be used to display images using base64
    base64_bin = models.BinaryField(null=True)
    # location_data
    panels = [ImageChooserPanel("image")]

    def save(self, *args, **kwargs):
        logger.info(f"base64 encoding image {self.image}")
        self.base64_bin = base64.b64encode(self.image.file.read())
        super().save(*args, **kwargs)


class PostImageSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(required=False)
    image = ImageRenditionField("fill-640x640")
    video = serializers.FileField()

    class Meta:
        model = PostImages
        fields = ["image", "video"]


class Post(Page):
    artists = ClusterTaggableManager(
        through="artists.PostArtist",
        blank=True,
        verbose_name="artist",
        related_name="artist_posts",
    )
    tags = ClusterTaggableManager(through="artists.PostTag", blank=True)
    uuid = models.UUIDField(null=True, unique=True, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel(
            "post_images",
            panels=[ImageChooserPanel("image"), VideoChooserPanel("video")],
            label="Post images",
        ),
        FieldPanel("artists", heading="artists"),
        FieldPanel("tags"),
    ]

    settings_panels = [
        FieldPanel("first_published_at", heading="Publish date")
    ] + Page.settings_panels
    context_object_name = "post"

    api_fields = [
        APIField("tags"),
        APIField("artists"),
        APIField("post_images", serializer=PostImageSerializer(many=True)),
    ]

    class Meta:
        ordering = ("-first_published_at",)

    @property
    def images(self):
        return self.post_images

    @property
    def image_urls(self):
        return self.post_images.all()

    @property
    def images_new(self):
        return self.post_images.filter(image_new__isnull=False)


class RichPost(Post):
    body = RichTextField(blank=True)  # this field is being removed

    content_panels = Post.content_panels + [
        FieldPanel("body"),
    ]
