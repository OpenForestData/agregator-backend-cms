from cms.extensions import PageExtension, extension_pool
from cms.models import Page
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField


class MetaTagsExtension(PageExtension):
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


# about us page

class MetaPage(models.Model):
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

class MainPage(MetaPage):
    og_image = FilerImageField(verbose_name="Miniatura w social Media", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='main_page_og_image')
    title_slider = models.CharField(max_length=120, verbose_name="Tytuł duży", unique=True)
    title_slider_small = models.CharField(max_length=120, verbose_name="Tytuł mały", unique=True)
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


class IconSpecies(models.Model):
    main_page = models.ForeignKey(MainPage, related_name="icon_species", on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Nazwa Gatunku")
    image = FilerImageField(verbose_name="Miniatura prezentująca gatunek", on_delete=models.CASCADE,
                            null=True, blank=True, related_name='species_image')
    order = models.IntegerField(max_length=10, default=1, verbose_name="Kolejność")


class FaqShort(models.Model):
    main_page = models.ForeignKey(MainPage, related_name="faq_shorts", on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Tytuł/Pytanie")
    anchor = models.CharField(max_length=500, default="#", verbose_name="Link do przekierowania po kliknięciu")
    order = models.IntegerField(max_length=10, default="1", verbose_name="Kolejność")


# accordion template

class AccordionPage(MetaPage):
    og_image = FilerImageField(verbose_name="Miniatura w social Media", on_delete=models.CASCADE,
                               null=True, blank=True, related_name='accordion_page_og_image')
    content = HTMLField(verbose_name="Content wpisu", null=True, blank=True)


class Accordion(models.Model):
    accordion_page = models.ForeignKey(AccordionPage, related_name="accordion_page", on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Tytuł")
    content = HTMLField(verbose_name="Content wpisu")
    order = models.IntegerField(max_length=10, default=1, verbose_name="Kolejność")


class PagePattern(models.Model):
    page = models.ForeignKey(Page, unique=True, verbose_name="Page",
                             editable=False, related_name='extended_fields', on_delete=models.CASCADE)
    about_us = models.OneToOneField(AboutUsPage, unique=True, verbose_name="Szablon o Nas", related_name='about_us',
                                    on_delete=models.CASCADE, null=True, blank=True)
    accordion = models.OneToOneField(AccordionPage, unique=True, verbose_name="Szablon z Akordionami",
                                     related_name="accordion", on_delete=models.CASCADE, null=True, blank=True)
