from cms.models import Title
from django.forms import ModelForm

from page_manager.models import PagePattern


class PagePatternAdminForm(ModelForm):
    """
    Page pattern class - used as relation to cms page
    """

    def __init__(self, *args, **kwargs):
        super(PagePatternAdminForm, self).__init__(*args, **kwargs)
        self.fields['title'].queryset = Title.objects.filter(page__publisher_is_draft=False)

    class Meta:
        model = PagePattern
        fields = '__all__'
