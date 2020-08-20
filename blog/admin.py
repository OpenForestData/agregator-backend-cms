from django.contrib import admin
from django.utils.text import slugify
from unidecode import unidecode
from blog.form import ArticleAdminForm
from blog.models import Article, BlogKeyword, BlogFront


class BlogFrontAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of BlogFront model in admin views
    """
    model = BlogFront

    def has_add_permission(self, request):
        """
        Method responsible for ensuring only MAX OBJECTS
        of BlogFront will be created
        """
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Method responsible for ensuring only MAX OBJECTS
        of BlogFront will be created
        """
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_delete_permission(request)


class ArticleAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of Article in admin views
    """
    model = Article
    exclude = ('slug',)
    ordering = ['language', 'date']
    form = ArticleAdminForm
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )

    def save_model(self, request, obj, form, change):
        """
        Method responsible for ensure slug in article will be always
        a slug based on article title
        """
        obj.slug = slugify(unidecode(obj.title))
        super(ArticleAdmin, self).save_model(request, obj, form, change)


admin.site.register(Article, ArticleAdmin)


class BlogKeyWordAdmin(admin.ModelAdmin):
    """
    Class responsible for representation of BlogKeyword model in admin views
    """
    model = BlogKeyword
    exclude = ('slug',)
    ordering = ['language']
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )

    def save_model(self, request, obj, form, change):
        """
        Method responsible for ensure slug in blog keyword will be always
        a slug based on blog keyword title
        """
        obj.slug = slugify(unidecode(obj.title))
        super(BlogKeyWordAdmin, self).save_model(request, obj, form, change)


admin.site.register(BlogKeyword, BlogKeyWordAdmin)
