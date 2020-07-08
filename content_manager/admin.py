from cms.extensions import TitleExtensionAdmin
from django.contrib import admin

from content_manager.models import Slide, ExtendedPage


class SlideInlineAdmin(admin.StackedInline):
    model = Slide


class ExtendedPageAdmin(TitleExtensionAdmin):
    pass


admin.site.register(ExtendedPage, ExtendedPageAdmin)
