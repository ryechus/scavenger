from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Prefetch
from posts.models import Post
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.images import get_image_model


class HomePage(Page):
    spotlight_post = models.ForeignKey(
        "posts.Post",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="spotlight_parent",
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        renditions_queryset = (
            get_image_model().get_rendition_model().objects.filter(filter_spec__in=["fill-640x640"])
        )
        posts = (
            Post.objects.child_of(self)
            .live()
            .filter(spotlight_parent__isnull=True)
            .prefetch_related(Prefetch("post_images__image__renditions", queryset=renditions_queryset))
            .prefetch_related(Prefetch("tags"))
            .prefetch_related(Prefetch("artists"))
            .order_by("-first_published_at")
        )
        paginator = Paginator(posts, 12)

        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        return context

    content_panels = Page.content_panels + [
        FieldPanel("spotlight_post"),
    ]
