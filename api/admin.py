from django.contrib import admin

# Register your models here.
from api.models import FacetField, FilterGroup, FilterField, AgregatorCategory


class FacetFieldAdmin(admin.ModelAdmin):
    model = FacetField
    ordering = ['order']


admin.site.register(FacetField, FacetFieldAdmin)


class FilterFieldAdmin(admin.StackedInline):
    model = FilterField
    ordering = ['order']


class FilterGroupAdmin(admin.ModelAdmin):
    model = FilterGroup
    inlines = [FilterFieldAdmin, ]


admin.site.register(FilterGroup, FilterGroupAdmin)


class AgregatorCategoryAdmin(admin.ModelAdmin):
    model = AgregatorCategory
    ordering = ['order']


admin.site.register(AgregatorCategory, AgregatorCategoryAdmin)
