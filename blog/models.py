from django.db import models

# Create your models here.
from django.urls import reverse
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from core.base_models import LangChooseMixin


class BlogFront(models.Model):
    title = models.CharField(max_length=120, verbose_name="Tytuł", unique=True)
    image = FilerImageField(verbose_name="Obrazek górny", on_delete=models.CASCADE,
                            null=True, blank=True, related_name='image_for_blog_top')
    title_seo = models.CharField(max_length=500, verbose_name="Tytuł (nadpisuje podstawowy tytuł)", null=True,
                                 blank=True)
    description = models.CharField(max_length=500, verbose_name="Opis (nadpisuje podstawowy opis)", null=True,
                                   blank=True)
    keywords_seo = models.CharField(max_length=500, verbose_name="Keywords", null=True,
                                    blank=True)
    author = models.CharField(max_length=500, verbose_name="Autor", null=True,
                              blank=True)
    og_type = models.CharField(max_length=15, verbose_name="Og:Type - według dokumentacji: https://ogp.me/", null=True,
                               blank=True)
    og_image = FilerImageField(verbose_name="Miniatura w social Media", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='blog_index_og_image')

    class Meta:
        verbose_name_plural = "Blog Top"
        verbose_name = "Blog Top"

    def __str__(self):
        return self.title


class BlogKeyword(LangChooseMixin):
    title = models.CharField(max_length=120, verbose_name="Tag", unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Tagi"
        verbose_name = "Tag"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('api:blog:keyword', kwargs={'slug': self.slug})

    def get_articles(self):
        return self.blog_articles.all().order_by('date')


class Article(LangChooseMixin):
    title_seo = models.CharField(max_length=500, verbose_name="Tytuł (nadpisuje podstawowy tytuł)", null=True,
                                 blank=True)
    description = models.CharField(max_length=500, verbose_name="Opis (nadpisuje podstawowy opis)", null=True,
                                   blank=True)
    keywords_seo = models.CharField(max_length=500, verbose_name="Keywords", null=True,
                                    blank=True)
    author = models.CharField(max_length=500, verbose_name="Autor", null=True,
                              blank=True)
    og_type = models.CharField(max_length=15, verbose_name="Og:Type - według dokumentacji: https://ogp.me/", null=True,
                               blank=True)
    og_image = FilerImageField(verbose_name="Miniatura w social Media", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='article_og_image')
    image_in_list = FilerImageField(verbose_name="Obrazek na liście bloga", on_delete=models.CASCADE,
                                    null=True, blank=True, related_name='image_in_list')
    title = models.CharField(max_length=120, verbose_name="Tytuł", unique=True)
    date = models.DateField(auto_now_add=True, verbose_name="Data utworzenia")
    desc = HTMLField(verbose_name="Opis do listy", null=True, blank=True)
    keywords = models.ManyToManyField(BlogKeyword, related_name="blog_articles")
    content = HTMLField(verbose_name="Content wpisu - <name> zostanie zamienione na imię", null=True, blank=True)
    movie_youtube_link = models.CharField(max_length=120, verbose_name="Link do filmu na YT", null=True, blank=True)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Artykuły"
        verbose_name = "Artykuł"

    def __str__(self):
        return self.title + f" {str(self.date)}"

    def get_content(self, name):
        return str(self.content).replace('{imie}', f'<strong>{name}</strong>')

    def get_content2(self, name):
        return ""

    def get_absolute_url(self):
        return reverse('api:blog:detail', kwargs={'slug': self.slug})

    def personalize(self, text, name):
        return str(text).replace('{imie}', f'<strong>{name}</strong>')

    def next_prev_get(self):
        qset = list(self.__class__.objects.all().order_by('date'))
        obj_index = qset.index(self)
        try:
            previous = qset[obj_index - 1]
        except IndexError:
            previous = None
        try:
            next = qset[obj_index + 1]
        except IndexError:
            next = None
        return previous, next
