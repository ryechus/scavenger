from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from posts.models import Post
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page


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
        posts = (
            Post.objects.child_of(self)
            .live()
            .filter(spotlight_parent__isnull=True)
            .order_by("-first_published_at")
        )
        paginator = Paginator(posts, 25)

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
