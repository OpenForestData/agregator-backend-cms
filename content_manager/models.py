from cms.extensions import TitleExtension, extension_pool
from cms.models import CMSPlugin
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from content_manager.base_model_classess import ImageMixin


################################################################################

#                                   SLIDER

################################################################################


class SliderPlugin(CMSPlugin):
    """
    Plugin model responsible for choosing proper Sldier class isntance
    """
    pass


class Slide(ImageMixin):
    """
    Slide class responsible for handle slide data
    """
    slider = models.ForeignKey(SliderPlugin, related_name='slides', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Tytuł slidera duży")
    small_title = models.CharField(max_length=120, verbose_name="Tytuł slidera mały")
    link = models.CharField(max_length=120, verbose_name="Link slidera")
    menu_title = models.CharField(max_length=120, verbose_name="Tytuł w menu slidera")
    menu_title_small = models.CharField(max_length=120, verbose_name="Tytuł szary w menu slidera")
    content = HTMLField(null=True, blank=True, verbose_name="Content po kliknięciu plusa")
    content_image = FilerImageField(verbose_name="Zdjęcie po kliknięciu w cotntent", on_delete=models.CASCADE,
                                    null=True, blank=True, related_name='content_image')


class ExtendedPage(TitleExtension):
    my_extra_field = models.CharField(max_length=120)


extension_pool.register(ExtendedPage)
