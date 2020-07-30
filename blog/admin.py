from django.contrib import admin

# Register your models here.
from django.utils.text import slugify
from unidecode import unidecode

from blog.form import ArticleAdminForm
from blog.models import Article, BlogKeyword, BlogFront


class BlogFrontAdmin(admin.ModelAdmin):
    model = BlogFront

    def has_add_permission(self, request):
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        MAX_OBJECTS = 1
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_delete_permission(request)


# admin.site.register(BlogFront, BlogFrontAdmin)


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    exclude = ('slug',)
    ordering = ['language', 'date']
    form = ArticleAdminForm
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(unidecode(obj.title))
        super(ArticleAdmin, self).save_model(request, obj, form, change)


admin.site.register(Article, ArticleAdmin)


class BlogKeyWordAdmin(admin.ModelAdmin):
    model = BlogKeyword
    exclude = ('slug',)
    ordering = ['language']
    list_filter = (
        ('language', admin.AllValuesFieldListFilter),
    )

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(unidecode(obj.title))
        super(BlogKeyWordAdmin, self).save_model(request, obj, form, change)


admin.site.register(BlogKeyword, BlogKeyWordAdmin)
