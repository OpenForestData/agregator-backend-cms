from cms.extensions import PageExtensionAdmin
from cms.models import Page
from django.contrib import admin

from page_manager.models import MetaTagsExtension, AboutUsPage


class MetaTagsExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(MetaTagsExtension, MetaTagsExtensionAdmin)


class AboutUsPageAdmin(admin.ModelAdmin):
    model = AboutUsPage

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['page'].queryset = Page.objects.published()
        return super(AboutUsPageAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(AboutUsPage, AboutUsPageAdmin)
