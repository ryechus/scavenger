from wagtail.contrib.modeladmin.options import ModelAdmin

from .models import HomePage


class HomeAdmin(ModelAdmin):
    model = HomePage
    list_display = ("title",)
