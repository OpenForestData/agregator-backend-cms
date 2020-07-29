from cms.extensions import PageExtension, extension_pool
from cms.models import Title
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from easy_thumbnails.files import get_thumbnailer
from filer.fields.image import FilerImageField

from core.base_models import LangChooseMixin


class MetaTagsExtension(PageExtension):
    """
    Page extension for ensuring seo meta tags
    """
    title = models.CharField(max_length=500, verbose_name="Tytuł (nadpisuje podstawowy tytuł)", null=True, blank=True)
    description = models.CharField(max_length=500, verbose_name="Opis (nadpisuje podstawowy opis)", null=True,
                                   blank=True)
    keywords = models.CharField(max_length=500, verbose_name="Keywords", null=True,
                                blank=True)
    author = models.CharField(max_length=500, verbose_name="Autor", null=True,
                              blank=True)
    og_type = models.CharField(max_length=15, verbose_name="Og:Type - według dokumentacji: https://ogp.me/", null=True,
                               blank=True)
    og_image = FilerImageField(verbose_name="Miniatura w social Media", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='og_image')


extension_pool.register(MetaTagsExtension)


class MetaPage(models.Model):
    """
    Model responsible for storing data for SEO model of each page
    """
    title = models.CharField(max_length=120, verbose_name="Tytuł", unique=True)
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

    class Meta:
        verbose_name_plural = "Blog Top"
        verbose_name = "Blog Top"
        abstract = True

    def __str__(self):
        return self.title


class AboutUsPage(MetaPage):
    og_image = FilerImageField(verbose_name="Miniatura w social Media", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='about_page_og_image')
    title = models.CharField(max_length=120, verbose_name="Tytuł", unique=True)
    content = HTMLField(verbose_name="Content wpisu")


# end of about us page

class MainPage(MetaPage, LangChooseMixin):
    """
    Model responsible for storing Main Page model data
    """
    og_image = FilerImageField(verbose_name="Miniatura w social Media", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='main_page_og_image')
    title_slider = models.CharField(max_length=120, verbose_name="Tytuł duży")
    title_slider_small = models.CharField(max_length=120, verbose_name="Tytuł mały")
    contact_content = models.TextField(verbose_name="Tekst do kontaktu")
    # youtube section
    youtube_title = models.CharField(max_length=120, verbose_name="Nazwa sekcji YouTube")
    youtube_link = models.CharField(max_length=500, verbose_name="Link do filmu na YouTube")
    youtube_mobie_text = models.CharField(max_length=120, verbose_name="Podpis pod filmem z YouTube")
    # mobile app section
    mobile_app_title = models.CharField(max_length=120, verbose_name="Tytuł sekcji aplikacja mobilna")
    mobile_app_content = models.TextField(verbose_name="Zawartość sekcji aplikacja mobilna", max_length=900)
    mobile_app_image = FilerImageField(verbose_name="Miniatura prezentująca aplikacje", on_delete=models.CASCADE,
                                       null=True, blank=True, related_name='mobile_app_image')
    mobile_app_cta_link = models.CharField(max_length=120, verbose_name="Link na przycisku")
    mobile_app_cta_text = models.CharField(max_length=120, verbose_name="Tekst na przycisku")

    class Meta:
        verbose_name = "Strona główna"
        verbose_name_plural = "Strona główna"


class IconSpecies(models.Model):
    """
    Model responsible for storing icon species for main page
    """
    main_page = models.ForeignKey(MainPage, related_name="icon_species", on_delete=models.CASCADE)
    href = models.CharField(max_length=300, verbose_name="Link do przekierowania", default="#")
    title = models.CharField(max_length=120, verbose_name="Nazwa Gatunku")
    image = FilerImageField(verbose_name="Miniatura prezentująca gatunek", on_delete=models.CASCADE,
                            null=True, blank=True, related_name='species_image')
    order = models.IntegerField(max_length=10, default=1, verbose_name="Kolejność")


class FaqShort(models.Model):
    """
    Model responsible for storing data schema for Faq short
    """
    main_page = models.ForeignKey(MainPage, related_name="faq_shorts", on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Tytuł/Pytanie")
    content = HTMLField(default="Faq content")
    anchor = models.CharField(max_length=500, default="#", verbose_name="Link do przekierowania po kliknięciu")
    order = models.IntegerField(max_length=10, default="1", verbose_name="Kolejność")


class AccordionPage(MetaPage):
    """
    Model responsible for storing data schema for accordion template page
    """
    og_image = FilerImageField(verbose_name="Miniatura w social Media", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='accordion_page_og_image')
    content = HTMLField(verbose_name="Content wpisu", null=True, blank=True)


class Accordion(models.Model):
    """
    Basic model responsible for storing accordion structure
    """
    accordion_page = models.ForeignKey(AccordionPage, related_name="accordion_page", on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Tytuł")
    content = HTMLField(verbose_name="Content wpisu")
    order = models.IntegerField(max_length=10, default=1, verbose_name="Kolejność")


class PagePattern(models.Model):
    """
    Model responsible for storing template and relate it with proper CMS page
    """
    title = models.ForeignKey(Title, unique=True, verbose_name="Strona",
                              editable=True, on_delete=models.CASCADE, related_name="page_patterns")
    about_us = models.OneToOneField(AboutUsPage, unique=True, verbose_name="Szablon o Nas", related_name='about_us',
                                    on_delete=models.CASCADE, null=True, blank=True)
    accordion = models.OneToOneField(AccordionPage, unique=True, verbose_name="Szablon z Akordionami",
                                     related_name="accordion", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title.title + " " + self.title.language

    class Meta:
        verbose_name_plural = "Szablony stron"
        verbose_name = "Szablon strony"

    def get_json_data(self):
        if self.about_us_id is not None:
            try:
                og_image_thumb_url = get_thumbnailer(self.about_us.og_image).get_thumbnail(
                    {'size': (1200, 630), 'crop': True}).url
            except Exception as ex:
                print(ex)
                og_image_thumb_url = ""
            page_pattern_data = {
                'title_seo': self.about_us.title_seo,
                'description': self.about_us.description,
                'keywords_seo': self.about_us.keywords_seo,
                'author': self.about_us.author,
                'og_type': self.about_us.og_type,
                'og_image': og_image_thumb_url,
                'title': self.about_us.title,
                'content': self.about_us.content,
            }

        if self.accordion_id is not None:
            accordion_page = AccordionPage.objects.filter(pk=self.accordion_id).first()

            options = {'size': (1200, 630), 'crop': True}
            try:
                og_image_thumb_url = get_thumbnailer(accordion_page.og_image).get_thumbnail(options).url
            except Exception as ex:
                print(ex)
                og_image_thumb_url = ""
            page_pattern_data = {
                'title_seo': accordion_page.title_seo,
                'description': accordion_page.description,
                'keywords_seo': accordion_page.keywords_seo,
                'author': accordion_page.author,
                'og_type': accordion_page.og_type,
                'og_image': og_image_thumb_url,
                'title': accordion_page.title,
                'content': accordion_page.content,
                'accordions': [{'title': accordion.title, 'content': accordion.content} for accordion in
                               Accordion.objects.filter(accordion_page=accordion_page).order_by('order')]
            }
        return page_pattern_data
