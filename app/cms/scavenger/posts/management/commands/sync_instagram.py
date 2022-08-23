import asyncio
import hashlib
import urllib.parse
from itertools import chain

import pendulum
from artists.models import ArtistTag
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from instagram_sync.contrib.django.models import InstagramAccount
from instagram_sync.core.graph_api.instagram import get_media, parse_caption
from PIL import Image as PILImage
from PIL import UnidentifiedImageError
from posts.models import Post, PostImages
from ripcurl.requests import get_content
from wagtail.core.models import Page, Site
from wagtail.images import get_image_model


class Command(BaseCommand):
    help = "Syncs instagram accounts"

    async def _handle(self, media, chunk_size=30):
        # get all instagram media
        results = []
        if len(media) > chunk_size:
            print("breaking into chunks")
            page = 1
            upper_bound = (len(media) // chunk_size) + 1
            while page <= upper_bound:
                print(f"chunk {page}")
                start_idx = (page - 1) * chunk_size
                end_idx = (page) * chunk_size
                page += 1
                downloaded_media = await asyncio.gather(
                    *[get_content(d["media_url"]) for d in media[start_idx:end_idx]]
                )
                results.append(downloaded_media)
        else:
            downloaded_media = await asyncio.gather(*[get_content(d["media_url"]) for d in media])

            results.append(downloaded_media)

        return results

    @staticmethod
    def add_content_from_media(image_files, ig_media_objects, page):
        images = []
        post_images = []

        # for each media request data
        image_model = get_image_model()
        for pair in zip(chain(*image_files), ig_media_objects):
            resp, m = pair
            content = resp.content
            split_url = urllib.parse.urlparse(m["media_url"]).path.split("/")
            title = split_url[-1].rsplit(".")[0]
            content_file = ContentFile(content, name=split_url[-1])
            try:
                pil_img = PILImage.open(content_file)
            except UnidentifiedImageError:
                print(f"error opening {m['media_url']}")
                continue
            img = image_model(
                title=title,
                file=content_file,
                width=pil_img.width,
                height=pil_img.height,
                file_hash=hashlib.sha1(content).hexdigest(),
            )
            caption_data = parse_caption(m["caption"])

            title = caption_data["title"]
            if title.strip():
                if not slugify(title):
                    title += "| placeholder"
                post = Post(title=title, first_published_at=pendulum.parse(m["timestamp"]), live=False)
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
        parser.add_argument("--site", type=str)

    def handle(self, *args, **options):
        # get ig account by account id
        ig_account = self.select_ig_account(account_id=options.get("ig_account_id"))
        print(f"import from ig account {ig_account.account_id}")

        selected_site = self.select_site(site_id=options.get("site_id"))
        root_page = selected_site.root_page
        # # get all instagram media
        media = get_media(ig_account.account_id, ig_account.access_token)["data"][::-1]
        print(f"importing {len(media)} instagram posts")

        downloaded_media = asyncio.run(self._handle(media, chunk_size=5))

        self.add_content_from_media(downloaded_media, media, root_page)

        print(f"done importing from ig account {ig_account.account_id}")
