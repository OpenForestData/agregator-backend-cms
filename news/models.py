import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer
from filer.fields.image import FilerImageField

from core.base_models import LangChooseMixin


class News(LangChooseMixin):
    """
    Class responsible for News model db structure
    """
    title_seo = models.CharField(max_length=500,
                                 verbose_name="Tytuł (nadpisuje podstawowy tytuł)",
                                 null=True,
                                 blank=True)
    description = models.CharField(max_length=500,
                                   verbose_name="Opis (nadpisuje podstawowy opis)",
                                   null=True,
                                   blank=True)
    keywords_seo = models.CharField(max_length=500, verbose_name="Keywords", null=True,
                                    blank=True)
    author = models.CharField(max_length=500, verbose_name="Autor", null=True,
                              blank=True)
    og_type = models.CharField(max_length=15,
                               verbose_name="Og:Type - według dokumentacji: https://ogp.me/",
                               null=True,
                               blank=True)
    og_image = FilerImageField(verbose_name="Miniatura w social Media",
                               on_delete=models.CASCADE,
                               null=True, blank=True, related_name='news_og_image')
    # thumbnail
    image_in_list = FilerImageField(verbose_name="Obrazek na liście bloga",
                                    on_delete=models.CASCADE,
                                    null=True, blank=True,
                                    related_name='image_in_list_news')
    title = models.CharField(max_length=120, verbose_name="Tytuł", unique=True)
    date = models.DateField(verbose_name="Data utworzenia", default=datetime.date.today)
    desc = RichTextUploadingField(verbose_name="Opis do listy", null=True, blank=True)
    content = RichTextUploadingField(verbose_name="Content wpisu", null=True, blank=True)
    slug = models.SlugField(max_length=500)

    class Meta:
        verbose_name_plural = "Newsy"
        verbose_name = "News"

    def __str__(self):
        return self.title + f" {str(self.date)} | {self.language}"

    def get_slug(self) -> str:
        """
        Method responsible for getting slug of article
        :return: slug: str
        """
        return self.slug

    def get_absolute_url(self) -> str:
        """
        Method responsible for getting absolute url to news
        :return: url: str
        """
        return reverse('api:news:detail', kwargs={'slug': self.slug})

    def next_prev_get(self) -> tuple:
        """
        Method responsible for getting next and previous news based on
        news instance
        :return: tuple of two newses
        """
        qset = list(self.__class__.objects.get_by_lang(self.language).order_by('date'))
        obj_index = qset.index(self)
        try:
            previous_news = qset[obj_index - 1]
        except IndexError:
            previous_news = None
        try:
            next_news = qset[obj_index + 1]
        except IndexError:
            next_news = None
        return previous_news, next_news

    def get_image_in_list_url(self) -> str:
        """
        Method responsible for creating link to thumbnail in list based
        on CMS user's subject location
        :return: str: url to image
        """
        url = ""
        if self.image_in_list:
            options = {'size': (1800, 1600), 'crop': True,
                       'subject_location': self.image_in_list.subject_location if self.image_in_list else None}
            url = get_thumbnailer(self.image_in_list).get_thumbnail(options).url
        return url

    def get_og_image_thumb_url(self) -> str:
        """
        Method responsible for creating link to thumbnail in SEO og image
        based on CMS user's subject location
        :return: str: url to image
        """
        url = ""
        if self.og_image:
            options = {'size': (1800, 1600), 'crop': True,
                       'subject_location': self.og_image.subject_location if self.image_in_list else None}
            url = get_thumbnailer(self.og_image).get_thumbnail(options).url
        return url

    def get_content(self) -> dict:
        """
        Method responsible for getting content of news
        :return:
        """
        next_news, prev_news = self.next_prev_get()

        article = {
            'title_seo': self.title_seo,
            'description': self.description,
            'keywords_seo': self.keywords_seo,
            'author': self.author,
            'og_type': self.og_type,
            'og_image': self.get_og_image_thumb_url(),
            'image_in_list': self.get_image_in_list_url(),
            'title': self.title,
            'date': self.date,
            'content': self.content,
            'url': self.get_absolute_url(),
            'slug': self.get_slug(),
            'next': next_news.get_slug() if next_news else None,
            'prev': prev_news.get_slug() if prev_news else None
        }
        return article


class NewsFront(models.Model):
    """
    Class responsible for storing data for news SEO meta tags in news list view
    """
    title = models.CharField(max_length=120, verbose_name="Tytuł", unique=True)
    image = FilerImageField(verbose_name="Obrazek górny", on_delete=models.CASCADE,
                            null=True, blank=True, related_name='image_for_news_top')
    title_seo = models.CharField(max_length=500,
                                 verbose_name="Tytuł (nadpisuje podstawowy tytuł)",
                                 null=True,
                                 blank=True)
    description = models.CharField(max_length=500,
                                   verbose_name="Opis (nadpisuje podstawowy opis)",
                                   null=True,
                                   blank=True)
    keywords_seo = models.CharField(max_length=500, verbose_name="Keywords", null=True,
                                    blank=True)
    author = models.CharField(max_length=500, verbose_name="Autor", null=True,
                              blank=True)
    og_type = models.CharField(max_length=15,
                               verbose_name="Og:Type - według dokumentacji: https://ogp.me/",
                               null=True,
                               blank=True)
    og_image = FilerImageField(verbose_name="Miniatura w social Media",
                               on_delete=models.CASCADE,
                               null=True, blank=True, related_name='news_index_og_image')
