from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path("tag/<str:tag>", views.get_posts_by_tag, name="tags"),
]
