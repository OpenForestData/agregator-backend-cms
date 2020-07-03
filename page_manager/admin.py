from cms.admin.pageadmin import PageAdmin
from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin
from cms.models import Page, Title
from django.contrib import admin

from page_manager.form import PagePatternAdminForm
from page_manager.models import MetaTagsExtension, AboutUsPage, PagePattern, MetaPage, MainPage, \
    IconSpecies, FaqShort, Accordion, AccordionPage


class MetaTagsExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(MetaTagsExtension, MetaTagsExtensionAdmin)


class MetaAdmin(admin.StackedInline):
    model = MetaPage


class AboutUsPageAdmin(admin.ModelAdmin):
    model = AboutUsPage


admin.site.register(AboutUsPage, AboutUsPageAdmin)


class PagePatternAdmin(admin.TabularInline):
    model = PagePattern
    form = PagePatternAdminForm


admin.site.unregister(Page)

PageAdmin.inlines.append(PagePatternAdmin)
admin.site.register(Page, PageAdmin)


class IconSpeciesAdmin(admin.StackedInline):
    model = IconSpecies


class FaqShortAdmin(admin.StackedInline):
    model = FaqShort
    ordering = ['order']


class MainPageAdmin(admin.ModelAdmin):
    model = MainPage
    inlines = [IconSpeciesAdmin, FaqShortAdmin]

    def has_add_permission(self, request):
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_delete_permission(request)


admin.site.register(MainPage, MainPageAdmin)


class AccordionAdmin(admin.StackedInline):
    model = Accordion
    ordering = ['order']


class AccordionPageAdmin(admin.ModelAdmin):
    model = AccordionPage
    inlines = [AccordionAdmin, ]


admin.site.register(AccordionPage, AccordionPageAdmin)
