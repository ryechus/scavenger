from django.db import models

from wagtail.core.models import Page

from posts.models import Post


class HomePage(Page):
    pass

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = (
            Post.objects.child_of(self).live().order_by("-first_published_at")
        )
        return context
