from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase
from wagtail.snippets.models import register_snippet


class ArtistTag(TagBase):
    class Meta:
        verbose_name = "artist"
        verbose_name_plural = "artists"


class Artist(ItemBase):
    name = models.CharField(max_length=100)
    tag = models.ForeignKey(ArtistTag, on_delete=models.CASCADE, related_name="tagged_artist")

    content_object = ParentalKey(to="posts.Post", on_delete=models.CASCADE, related_name="post_artists")

    def __str__(self):
        return self.name
