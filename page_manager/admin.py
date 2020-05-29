from cms.extensions import PageExtensionAdmin
from django.contrib import admin

from page_manager.models import MetaTagsExtension


class MetaTagsExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(MetaTagsExtension, MetaTagsExtensionAdmin)