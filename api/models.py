from django.db import models


class FacetField(models.Model):
    """
    Model responsible for storing data about used facet
    fields in agregator
    """
    facet_field_name = models.CharField(max_length=120, verbose_name="Nazwa pola w Solr")
    facet_field_friendly_name = models.CharField(max_length=120, verbose_name="Nazwa przyjazna")
    order = models.IntegerField(default=1, verbose_name="Kolejność")

    class Meta:
        verbose_name_plural = "Pola filtrowalne"
        verbose_name = "Pole filtrowalne"

    def __str__(self):
        return self.facet_field_friendly_name
