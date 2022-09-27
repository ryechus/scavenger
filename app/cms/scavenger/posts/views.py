from django.shortcuts import render  # noqa
from posts.models import Post


def get_posts_by_tag(request, tag):
    posts = Post.objects.filter(tags__name__iexact=tag)

    return render(request, "posts/tags.html", context={"posts": posts, "tag": tag})


def get_posts_by_artist_name(request, artist_name):
    posts = Post.objects.filter(artists__name__iexact=artist_name)

    return render(
        request, "posts/tags.html", context={"posts": posts, "tag": artist_name}
    )
