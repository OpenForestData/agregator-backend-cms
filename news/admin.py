from django.contrib import admin
from django.utils.text import slugify
from unidecode import unidecode
from news.models import News


class NewsAdmin(admin.ModelAdmin):
    model = News
    exclude = ('slug',)

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(unidecode(obj.title))
        super(NewsAdmin, self).save_model(request, obj, form, change)


admin.site.register(News, NewsAdmin)
