from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase, TaggedItemBase


class PostTag(TaggedItemBase):
    content_object = ParentalKey("posts.Post", on_delete=models.CASCADE)


class ArtistTag(TagBase):
    instagram_username = models.CharField(max_length=100, null=True)

    @property
    def instagram_href(self):
        return f"https://instagram.com/{self.instagram_username}"

    class Meta:
        verbose_name = "artist"
        verbose_name_plural = "artists"


class PostArtist(ItemBase):
    tag = models.ForeignKey(ArtistTag, on_delete=models.CASCADE, related_name="tagged_artist")

    content_object = ParentalKey(to="posts.Post", on_delete=models.CASCADE, related_name="post_artists")

    def __str__(self):
        return self.name
