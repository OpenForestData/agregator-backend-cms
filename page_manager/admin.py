from cms.extensions import PageExtensionAdmin
from django.contrib import admin

from core.settings import LANGUAGES
from page_manager.form import PagePatternAdminForm
from page_manager.models import MetaTagsExtension, AboutUsPage, PagePattern, MetaPage, MainPage, \
    IconSpecies, FaqShort, Accordion, AccordionPage


class MetaTagsExtensionAdmin(PageExtensionAdmin):
    """
    Class responsible for representation of
    PageExtension in admin views
    """
    pass


admin.site.register(MetaTagsExtension, MetaTagsExtensionAdmin)


class MetaAdmin(admin.StackedInline):
    """
    Class responsible for representation of
    MetaAdmin in admin views
    """
    model = MetaPage


class AboutUsPageAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of
    AboutUsPage in admin views
    """
    model = AboutUsPage


admin.site.register(AboutUsPage, AboutUsPageAdmin)


class PagePatternAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of
    PagePattern in admin views
    """
    model = PagePattern
    form = PagePatternAdminForm


admin.site.register(PagePattern, PagePatternAdmin)


class IconSpeciesAdmin(admin.StackedInline):
    """
    Class responsible for representation of
    IconSpecies in admin views
    """
    model = IconSpecies
    ordering = ['order']


class FaqShortAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of
    FaqShort in admin views
    """
    model = FaqShort
    ordering = ['order']
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )


admin.site.register(FaqShort, FaqShortAdmin)


class MainPageAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of
    MainPage in admin views
    """
    model = MainPage
    inlines = [IconSpeciesAdmin]
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )

    def has_add_permission(self, request):
        """
        Method responsible for ensuring only exactly the same
        amount of MainPage instances will be created as the amount
        of declared languages in system
        :param request: request
        """
        MAX_OBJECTS = len(LANGUAGES)
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Method responsible for ensuring only exactly the same
        amount of MainPage instances will be created as the amount
        of declared languages in system
        :param request: request
        """
        MAX_OBJECTS = len(LANGUAGES)
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_delete_permission(request)


admin.site.register(MainPage, MainPageAdmin)


class AccordionAdmin(admin.StackedInline):
    """
    Class responsible for representation of
    Accordion in admin views
    """
    model = Accordion
    ordering = ['order']


class AccordionPageAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of
    AccordionPage in admin views
    """
    model = AccordionPage
    inlines = [AccordionAdmin, ]


admin.site.register(AccordionPage, AccordionPageAdmin)
