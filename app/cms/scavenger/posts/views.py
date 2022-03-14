from django.http import HttpResponse
from django.shortcuts import render  # noqa

from artists.models import PostTag
from posts.models import Post


def get_posts_by_tag(request, tag):
    posts = Post.objects.filter(tags__name=tag).order_by("-first_published_at")

    return render(request, "posts/tags.html", context={"posts": posts, "tag": tag})
