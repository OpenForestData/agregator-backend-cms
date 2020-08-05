from cms.extensions import PageExtensionAdmin
from django.contrib import admin

from core.settings import LANGUAGES
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


class PagePatternAdmin(admin.ModelAdmin):
    model = PagePattern
    form = PagePatternAdminForm

    def save_model(self, request, obj, form, change):
        super(PagePatternAdmin, self).save_model(request, obj, form, change)


admin.site.register(PagePattern, PagePatternAdmin)


class IconSpeciesAdmin(admin.StackedInline):
    model = IconSpecies
    ordering = ['order']


class FaqShortAdmin(admin.ModelAdmin):
    model = FaqShort
    ordering = ['order']
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )


admin.site.register(FaqShort, FaqShortAdmin)


class MainPageAdmin(admin.ModelAdmin):
    model = MainPage
    inlines = [IconSpeciesAdmin]
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )

    def has_add_permission(self, request):
        MAX_OBJECTS = len(LANGUAGES)
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        MAX_OBJECTS = len(LANGUAGES)
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
