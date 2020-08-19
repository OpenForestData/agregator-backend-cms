from cms.models import Title
from django.forms import ModelForm

from page_manager.models import PagePattern


class PagePatternAdminForm(ModelForm):
    """
    ModelForm responsible for properly show available
    Tile CMS instances in select field
    """

    def __init__(self, *args, **kwargs):
        super(PagePatternAdminForm, self).__init__(*args, **kwargs)
        self.fields['title'].queryset = Title.objects.filter(page__publisher_is_draft=False)

    class Meta:
        model = PagePattern
        fields = '__all__'
