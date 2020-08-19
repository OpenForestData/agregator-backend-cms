from django.db import models

from core.settings import LANGUAGES


class LangObjectManager(models.Manager):
    """
    Manager responsible for obtaining specified language objects
    """
    def get_by_lang(self, language_alpha_2_code: str):
        return super().get_queryset().filter(language=language_alpha_2_code)


class LangChooseMixin(models.Model):
    """
    Abstract mixin to ensure model with language property
    """
    language = models.CharField(max_length=15, choices=LANGUAGES, default='pl')
    objects = LangObjectManager()

    class Meta:
        abstract = True
