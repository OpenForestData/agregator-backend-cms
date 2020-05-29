from cms.extensions import PageExtension, extension_pool
from django.db import models
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