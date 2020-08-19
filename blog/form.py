from django.forms import ModelForm

from blog.models import BlogKeyword, Article


class ArticleAdminForm(ModelForm):
    """
    Class responsible for form representation in admin panel
    """

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)
        self.fields['keywords'].queryset = BlogKeyword.objects.filter(language=self.instance.language)

    class Meta:
        model = Article
        fields = '__all__'
