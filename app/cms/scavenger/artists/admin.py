from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import ArtistTag, PostArtist


class ArtistsAdmin(ModelAdmin):
    model = ArtistTag
    menu_icon = "user"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ("name", "instagram", "posts")
    list_display_links = None
    list_editable = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display
    def posts(self, obj):
        path = reverse_lazy("posts:artist", args=[obj.name])
        html = f"<a href='{path}'>View Posts</a>"
        return mark_safe(html)

    @admin.display
    def instagram(self, obj):
        html = f"<a href='{obj.instagram_href}'>@{obj.instagram_username}</a>"
        return mark_safe(html)


@admin.register(ArtistTag)
class ArtistTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "instagram")
    list_editable = ("name",)

    @admin.display
    def instagram(self, obj):
        html = f"<a href='{obj.instagram_href}'>@{obj.instagram_username}</a>"
        return mark_safe(html)


modeladmin_register(ArtistsAdmin)
