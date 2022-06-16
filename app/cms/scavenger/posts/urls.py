from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path("artist/<str:artist_name>", views.get_posts_by_artist_name, name="artist"),
    path("tag/<str:tag>", views.get_posts_by_tag, name="tag"),
]
