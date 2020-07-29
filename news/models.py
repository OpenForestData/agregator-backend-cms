from django.db import models
from django.urls import reverse
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from core.base_models import LangChooseMixin


class News(LangChooseMixin):
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
                               null=True, blank=True, related_name='news_og_image')

    # thumbnail
    image_in_list = FilerImageField(verbose_name="Obrazek na liście bloga", on_delete=models.CASCADE,
                                    null=True, blank=True, related_name='image_in_list_news')
    title = models.CharField(max_length=120, verbose_name="Tytuł", unique=True)
    date = models.DateField(auto_now_add=True, verbose_name="Data utworzenia")
    desc = HTMLField(verbose_name="Opis do listy", null=True, blank=True)
    content = HTMLField(verbose_name="Content wpisu - <name> zostanie zamienione na imię", null=True, blank=True)
    # film
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Newsy"
        verbose_name = "News"

    def __str__(self):
        return self.title + f" {str(self.date)} | {self.language}"

    def get_absolute_url(self):
        return reverse('api:news:detail', kwargs={'slug': self.slug})

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


class NewsFront(models.Model):
    title = models.CharField(max_length=120, verbose_name="Tytuł", unique=True)
    image = FilerImageField(verbose_name="Obrazek górny", on_delete=models.CASCADE,
                            null=True, blank=True, related_name='image_for_news_top')
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
                               null=True, blank=True, related_name='news_index_og_image')
