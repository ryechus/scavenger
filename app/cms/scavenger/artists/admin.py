from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Artist


class ArtistsAdmin(ModelAdmin):
    model = Artist
    menu_icon = "user"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ("tag", "posts")
    search_fields = ("tag",)

    @admin.display
    def posts(self, obj):
        path = reverse_lazy("posts:artist", args=[obj.tag.name])
        html = f"<a href='{path}'>View Posts</a>"
        return mark_safe(html)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all().distinct("tag__name").order_by("tag__name")


modeladmin_register(ArtistsAdmin)
