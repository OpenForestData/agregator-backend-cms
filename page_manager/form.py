from django.forms import ModelForm

from page_manager.models import PagePattern


class PagePatternAdminForm(ModelForm):
    """
    Page pattern class - used as relation to cms page
    """

    class Meta:
        model = PagePattern
        exclude = ['page', ]
