import copy

from django.forms import ModelForm, forms

from page_manager.models import PagePattern


class PagePatternAdminForm(ModelForm):
    class Meta:
        model = PagePattern
        exclude = ['tag']
