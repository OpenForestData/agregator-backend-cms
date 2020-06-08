from cms.extensions import PageExtensionAdmin
from django.contrib import admin

from page_manager.models import MetaTagsExtension, AboutUsPage


class MetaTagsExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(MetaTagsExtension, MetaTagsExtensionAdmin)


class AboutUsPageAdmin(admin.ModelAdmin):
    model = AboutUsPage


admin.site.register(AboutUsPage, AboutUsPageAdmin)
