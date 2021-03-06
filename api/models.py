from django.db import models
from djangocms_text_ckeditor.fields import HTMLField

from core.base_models import LangChooseMixin


class AdvancedSearchFilterGroup(LangChooseMixin):
    """
    Model responsible for storing data about filter
    group fields - each group may have many fields
    """
    name = models.CharField(max_length=120, verbose_name="Nazwa pola w Dataverse")
    friendly_name = models.CharField(max_length=120, verbose_name="Nazwa przyjazna")
    order = models.IntegerField(default=1, verbose_name="Kolejność")

    class Meta:
        verbose_name_plural = "Grupy pól filtracyjnych - wyszukiwanie zaawansowane"
        verbose_name = "Grupa pól filtracyjnych - wyszkiwanie zaawansowane"

    def __str__(self):
        return self.name + f'| {self.language}'

    def get_fields(self):
        return list(self.fields.filter(public=True).order_by('order').values())


class AdvancedSearchFilterField(models.Model):
    """
    Model responsible for storing data about filter
    single field - each field has a relation with proper
    filter group
    """
    filter_group = models.ForeignKey(AdvancedSearchFilterGroup, related_name='fields',
                                     on_delete=models.CASCADE)
    field_name = models.CharField(max_length=120, verbose_name="Nazwa pola w Dataverse")
    friendly_name = models.CharField(max_length=120, verbose_name="Nazwa przyjazna")
    title = models.CharField(max_length=120, verbose_name="Tytuł")
    type = models.CharField(max_length=120, verbose_name="Rodzaj pola")
    watermark = models.CharField(max_length=120, verbose_name="Watermark", default="#")
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=1, verbose_name="Kolejność")
    public = models.BooleanField(default=True, verbose_name="Publiczny")

    def __str__(self):
        return self.field_name


class FilterGroup(LangChooseMixin):
    """
    Model responsible for storing data about filter
    group fields - each group may have many fields
    """
    name = models.CharField(max_length=120, verbose_name="Nazwa pola w Dataverse")
    friendly_name = models.CharField(max_length=120, verbose_name="Nazwa przyjazna")
    order = models.IntegerField(default=1, verbose_name="Kolejność")

    class Meta:
        verbose_name_plural = "Grupy pól filtracyjnych"
        verbose_name = "Grupa pól filtracyjnych"

    def __str__(self):
        return self.name + f'| {self.language}'

    def get_fields(self):
        return list(self.fields.filter(public=True).order_by('order').values())


class FilterField(models.Model):
    """
    Model responsible for storing data about filter
    single field - each field has a relation with proper
    filter group
    """
    filter_group = models.ForeignKey(FilterGroup, related_name='fields',
                                     on_delete=models.CASCADE)
    field_name = models.CharField(max_length=120, verbose_name="Nazwa pola w Dataverse")
    order = models.IntegerField(default=1, verbose_name="Kolejność")
    public = models.BooleanField(default=True, verbose_name="Publiczny")

    def __str__(self):
        return self.field_name


class AgregatorCategory(LangChooseMixin):
    """
    Model responsible for storing categories for agregator
    categories in searching and listing search results
    """
    dataverse_id = models.CharField(max_length=120, verbose_name="Dataverse Id")
    friendly_name = models.CharField(max_length=120, verbose_name="Nazwa przyjazna")
    description = HTMLField(null=True, blank=True)
    name = models.CharField(max_length=120, verbose_name="Name")
    dv_name = models.CharField(max_length=120, verbose_name="DvName")
    publication_date = models.CharField(max_length=10, verbose_name="Data publikacji")
    dv_affiliation = models.CharField(max_length=120,
                                      verbose_name="Dataverse Affiliation", null=True,
                                      blank=True)
    order = models.IntegerField(default=1, verbose_name="Kolejność")
    public = models.BooleanField(default=True, verbose_name="Publiczny")

    class Meta:
        verbose_name = "Kategoria Agregatora"
        verbose_name_plural = "Kategorie agregatora"

    def __str__(self):
        return self.friendly_name + f"| {self.language}"


class AddMenuLinks(LangChooseMixin):
    """
    Model responsible for creating menu of tabs in
    add resource small menu
    """
    name = models.CharField(max_length=120, verbose_name="Name", unique=True)
    url = models.CharField(max_length=220, verbose_name="Link")
    order = models.IntegerField(default=1, verbose_name="Kolejność")

    class Meta:
        verbose_name = "Dodanie resource (opcje)"
        verbose_name_plural = "Dodanie resourców (opcje)"

    def __str__(self):
        return self.name + f"| {self.language}"
