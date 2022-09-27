from django.contrib import admin  # noqa
from posts.models import Post
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register


class PostAdmin(ModelAdmin):
    model = Post
    menu_label = "Posts"  # ditch this to use verbose_name_plural from model
    menu_icon = "doc-empty"  # change as required
    menu_order = 100  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = ("title", "owner", "first_published_at")
    list_filter = ("owner",)
    search_fields = ("title", "owner", "first_published_at")


modeladmin_register(PostAdmin)
