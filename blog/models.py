from django.db import models
# Create your models here.
from django.urls import reverse
from djangocms_text_ckeditor.fields import HTMLField
from easy_thumbnails.files import get_thumbnailer
from filer.fields.image import FilerImageField

from core.base_models import LangChooseMixin


class BlogFront(models.Model):
    """
    Class responsible for BlogFront model db structure representation
    """
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
    """
    Class responsible for BlogKeyword model db structure representation
    """
    title = models.CharField(max_length=120, verbose_name="Tag")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Tagi"
        verbose_name = "Tag"

    def __str__(self):
        return self.title

    def get_slug(self) -> str:
        """
        Method responsible for getting slug of BlogKeyword
        :return: slug: str
        """
        return self.slug

    def get_absolute_url(self) -> str:
        """
        Method responsible for getting absolute url to
        list of articles based on keyword
        :return: url: str
        """
        return reverse('api:blog:keyword', kwargs={'slug': self.slug})

    def get_articles(self):
        """
        Method responsible for getting all related articles
        :return: articles: QuerySet<Article>
        """
        return self.blog_articles.all().order_by('date')


class Article(LangChooseMixin):
    """
    Class responsible for Article model db structure representation
    """
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
    content = HTMLField(verbose_name="Content wpisu", null=True, blank=True)
    movie_youtube_link = models.CharField(max_length=120, verbose_name="Link do filmu na YT", null=True, blank=True)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Artykuły"
        verbose_name = "Artykuł"

    def get_slug(self):
        """
        Method responsible for getting article slug
        :return:
        """
        return self.slug

    def __str__(self):
        return self.title + f" {str(self.date)}"

    def get_absolute_url(self):
        """
        Method responsible for getting absolute url to
        article instance
        :return: url: str
        """
        return reverse('api:blog:detail', kwargs={'slug': self.slug})

    def next_prev_get(self):
        """
        Method responsible for getting next_article and prev article objects
        :return: tuple of two Article instances
        """
        articles_list = list(self.__class__.objects.get_by_lang(self.language).order_by('date'))
        obj_index = articles_list.index(self)
        try:
            prev_article = articles_list[obj_index - 1]
        except IndexError:
            prev_article = None
        try:
            next_article = articles_list[obj_index + 1]
        except IndexError:
            next_article = None
        return prev_article, next_article

    def get_image_in_list_url(self) -> str:
        url = ""
        if self.image_in_list:
            options = {'size': (1800, 1600), 'crop': True,
                       'subject_location': self.image_in_list.subject_location if self.image_in_list else None}
            url = get_thumbnailer(self.image_in_list).get_thumbnail(options).url
        return url

    def get_og_image_thumb_url(self) -> str:
        url = ""
        if self.og_image:
            options = {'size': (1800, 1600), 'crop': True,
                       'subject_location': self.og_image.subject_location if self.image_in_list else None}
            url = get_thumbnailer(self.og_image).get_thumbnail(options).url
        return url

    def get_content(self):
        next_article, prev_article = self.next_prev_get()

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
            'keywords': [{'title': keyword.title, 'url': keyword.get_absolute_url(), 'slug': keyword.get_slug()} for
                         keyword in self.keywords.all()],
            'movie_youtube_link': self.movie_youtube_link,
            'url': self.get_absolute_url(),
            'slug': self.get_slug(),
            'next': next_article.get_slug() if next_article else None,
            'prev': prev_article.get_slug() if prev_article else None
        }
        return article
