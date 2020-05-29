from django.db import models
from filer.fields.image import FilerImageField

from core.settings import LANGUAGES


class LanguageMixin(models.Model):
    """
    Mixin responsbile for selecting language of each db instance
    """

    language = models.CharField(max_length=8, choices=LANGUAGES, default='pl')

    class Meta:
        abstract = True


class InstanceNameMixin(models.Model):
    """
    Mixin responsible for naming each instance and identify it in CMS
    """

    instance_name = models.CharField(max_length=120, verbose_name="Nazwa wyświetlana w CMS")

    class Meta:
        abstract = True


class BasicClassModel(InstanceNameMixin, LanguageMixin):
    """
    Basic model abstract class, must be parent of each class in content manager
    """

    class Meta:
        abstract = True

    def __str__(self):
        return self.instance_name + "|" + self.get_language_display()


class ImageMixin(models.Model):
    """
    Mixin responsbile for allowing using filer in class
    """
    image = FilerImageField(verbose_name="Zdjęcie", related_name='image', on_delete=models.CASCADE)

    class Meta:
        abstract = True
