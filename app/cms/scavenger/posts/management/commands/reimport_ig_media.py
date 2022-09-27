import logging

from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from images.models import ImageServiceImageModel
from posts.models import PostImages

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Re-imports Instagram media"

    def handle(self, *args, **options):
        for img in PostImages.objects.filter(
            post__uuid__isnull=False, image__isnull=False
        ):
            logger.info(f"re-importing {img.image.file.name}")
            new_image = ImageServiceImageModel.objects.get_or_create(
                title=img.image.title,
                file=ContentFile(img.image.file.read(), name=img.image.file.name),
                width=img.image.width,
                height=img.image.height,
            )[0]
            img.image_new = new_image
            img.save()
