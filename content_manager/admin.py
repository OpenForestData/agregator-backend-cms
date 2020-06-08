from cms.admin.pageadmin import PageAdmin
from cms.extensions import TitleExtensionAdmin
from cms.models.pagemodel import Page
from django.contrib import admin

# Register your models here.
from content_manager.models import Slide, ExtendedPage


class SlideInlineAdmin(admin.StackedInline):
    model = Slide


class ExtendedPageAdmin(TitleExtensionAdmin):
    pass


admin.site.register(ExtendedPage, ExtendedPageAdmin)
