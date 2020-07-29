from django.forms import ModelForm

from blog.models import BlogKeyword, Article


class ArticleAdminForm(ModelForm):
    """
    Page pattern class - used as relation to cms page
    """

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        self.fields['keywords'].queryset = BlogKeyword.objects.filter(language=self.instance.language)

    class Meta:
        model = Article
        fields = '__all__'
