from django.contrib import admin

# Register your models here.
from api.models import FilterGroup, FilterField, AgregatorCategory, AdvancedSearchFilterField, AdvancedSearchFilterGroup


class FilterFieldAdmin(admin.StackedInline):
    model = FilterField
    ordering = ['order']


class FilterGroupAdmin(admin.ModelAdmin):
    model = FilterGroup
    inlines = [FilterFieldAdmin, ]


admin.site.register(FilterGroup, FilterGroupAdmin)


class AdvancedSearchFilterFieldAdmin(admin.StackedInline):
    model = AdvancedSearchFilterField
    ordering = ['order']


class AdvancedSearchFilterGroupAdmin(admin.ModelAdmin):
    model = AdvancedSearchFilterGroup
    inlines = [AdvancedSearchFilterFieldAdmin, ]


admin.site.register(AdvancedSearchFilterGroup, AdvancedSearchFilterGroupAdmin)


class AgregatorCategoryAdmin(admin.ModelAdmin):
    model = AgregatorCategory
    ordering = ['order']


admin.site.register(AgregatorCategory, AgregatorCategoryAdmin)
