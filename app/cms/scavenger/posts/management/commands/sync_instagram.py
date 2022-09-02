import hashlib
import urllib.parse
import uuid

import pendulum
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from instagram_sync.contrib.django.models import InstagramAccount
from instagram_sync.core.graph_api.instagram import get_media, parse_caption
from instagram_sync.core.media import IGMediaCollection, IGMediaObject
from wagtail.core.models import Site
from wagtail.images import get_image_model

from artists.models import ArtistTag
from posts.models import Post, PostImages


class Command(BaseCommand):
    help = "Syncs instagram accounts"

    @staticmethod
    def add_content_from_media(media: list[IGMediaObject], page):
        images = []
        post_images = []

        # for each media request data
        image_model = get_image_model()
        for m in media:
            # resp, m = pair
            post = Post.objects.filter(uuid=uuid.uuid5(uuid.NAMESPACE_URL, m.graph.permalink)).first()
            if post:
                continue

            split_url = urllib.parse.urlparse(m.graph.media_url).path.split("/")
            title = split_url[-1].rsplit(".")[0]
            content_file = ContentFile(m.bytes, name=split_url[-1])

            if not m.width or not m.height:
                continue

            img = image_model(
                title=title,
                file=content_file,
                width=m.width,
                height=m.height,
                file_hash=hashlib.sha1(m.bytes).hexdigest(),
            )
            caption_data = parse_caption(m.graph.caption)

            title = caption_data["title"]
            if title.strip():
                if not slugify(title):
                    title += "| placeholder"

                post = Post(
                    title=title,
                    first_published_at=pendulum.parse(m.graph.timestamp),
                    uuid=uuid.uuid5(uuid.NAMESPACE_URL, m.graph.permalink),
                    live=False,
                )
                artists = []
                for artist in caption_data["artists"]:
                    artist_tag = ArtistTag.objects.get_or_create(instagram_username=artist)[0]
                    if not artist_tag.name:
                        artist_tag.name = artist
                        artist_tag.save()
                    artists.append(artist_tag)

                post.artists.add(*artists)
                post.tags.add(*caption_data["tags"])

                page.add_child(instance=post)

                post.save_revision().publish()

                post_image = PostImages(post=post, image=img)
                post_images.append(post_image)

                post.unpublish()

            images.append(img)

        image_model.objects.bulk_create(images)
        PostImages.objects.bulk_create(post_images)

    @staticmethod
    def select_ig_account(account_id=None):
        if account_id:
            return InstagramAccount.objects.get(pk=account_id)

        accounts = InstagramAccount.objects.all()
        for idx, site in enumerate(accounts):
            print(f"{idx}: {site.account_id}")

        selected_acct = input("Select an instagram account to sync?")
        selected_acct = accounts[int(selected_acct)] if selected_acct else accounts.first()

        return selected_acct

    @staticmethod
    def select_site(site_id=None):
        if site_id:
            return Site.objects.get(pk=site_id)

        sites = Site.objects.all()
        for idx, site in enumerate(sites):
            print(f"{idx}: {site.hostname}")

        selected_site = input("Which site would you like to sync instagram with?")
        selected_site = sites[int(selected_site)] if selected_site else sites.first()

        return selected_site

    def add_arguments(self, parser):
        parser.add_argument("--ig-account-id", type=int)
        parser.add_argument("--site-id", type=str)
        parser.add_argument("--lookback", type=int)

    def handle(self, *args, **options):
        # get ig account by account id
        ig_account = self.select_ig_account(account_id=options.get("ig_account_id"))
        print(f"import from ig account {ig_account.account_id}")

        selected_site = self.select_site(site_id=options.get("site_id"))
        root_page = selected_site.root_page

        since = int(pendulum.now("UTC").subtract(seconds=options.get("lookback", 30)).timestamp())
        # # get all instagram media
        media = get_media(ig_account.account_id, ig_account.access_token, since=since)["data"][::-1]
        collection = IGMediaCollection(media)
        ig_media = collection.collection
        print(f"importing {len(ig_media)} instagram posts")

        self.add_content_from_media(ig_media, root_page)

        print(f"done importing from ig account {ig_account.account_id}")
