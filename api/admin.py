from django.contrib import admin
from api.models import FilterGroup, FilterField, AgregatorCategory, AdvancedSearchFilterField, \
    AdvancedSearchFilterGroup, AddMenuLinks


class FilterFieldAdmin(admin.StackedInline):
    """
    Class responsible for representation of a FilterField model edition in FilterGroup admin views
    """
    model = FilterField
    ordering = ['order']


class FilterGroupAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of a FilterGroup model edition in admin views
    """
    model = FilterGroup
    inlines = [FilterFieldAdmin, ]
    ordering = ['language', 'order']
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )


admin.site.register(FilterGroup, FilterGroupAdmin)


class AdvancedSearchFilterFieldAdmin(admin.StackedInline):
    """
    Class responsible for representation of a AdvancedSearchFilterFields model edition in
    AdvancedSearchFilterGroup admin views
    """
    model = AdvancedSearchFilterField
    ordering = ['order']


class AdvancedSearchFilterGroupAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of a AdvancedSearchFilterGroup model in admin views
    """
    model = AdvancedSearchFilterGroup
    inlines = [AdvancedSearchFilterFieldAdmin, ]
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )


admin.site.register(AdvancedSearchFilterGroup, AdvancedSearchFilterGroupAdmin)


class AgregatorCategoryAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of a AgregatorCategory in admin Views
    """
    model = AgregatorCategory
    ordering = ['language', 'order']
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )


admin.site.register(AgregatorCategory, AgregatorCategoryAdmin)


class AddMenuLinksAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of a AddMenuLinks model in admin views
    """
    model = AddMenuLinks
    ordering = ['language', 'order']
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )


admin.site.register(AddMenuLinks, AddMenuLinksAdmin)
