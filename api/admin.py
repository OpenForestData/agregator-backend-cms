from django.contrib import admin

# Register your models here.
from api.models import FacetField


class FacetFieldAdmin(admin.ModelAdmin):
    model = FacetField
    ordering = ['order']


admin.site.register(FacetField, FacetFieldAdmin)
