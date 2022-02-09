from django.db import models
from wagtail.admin.edit_handlers import FieldPanel

from wagtail.core.models import Page

from posts.models import Post


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
        context["posts"] = (
            Post.objects.child_of(self)
            .live()
            .filter(spotlight_parent__isnull=True)
            .order_by("-first_published_at")
        )
        return context

    content_panels = Page.content_panels + [
        FieldPanel("spotlight_post"),
    ]
