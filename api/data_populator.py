import json

from api.models import FilterField, FilterGroup, AgregatorCategory, \
    AdvancedSearchFilterGroup, AdvancedSearchFilterField
from core.settings import LANGUAGES


class DataPopulator:
    """
    Class responsible for proper population of
    solr and dataverse data (metadata blocks and categories)
    """

    def populate_metadata_blocks(self, metadata_blocks: dict) -> bool:
        """
        Method responsible for populating metadata as filter group
        ensuring to add new fields
        :param metadata_blocks: dict with metadata blocks schema
        :return: bool, True if registration is complete
        """
        for lang_tuple in LANGUAGES:
            lang = lang_tuple[0]
            all_filter_groups_names = [filter_group['name'] for filter_group in
                                       FilterGroup.objects.get_by_lang(lang).values(
                                           'name')]
            al_filter_fields_names = []
            for filter_group in FilterGroup.objects.get_by_lang(lang):
                al_filter_fields_names += [filter_field['field_name'] for filter_field in
                                           filter_group.fields.all().values('field_name')]
            wrong_names = ['taxonomicCoverage']

            for metadata_name, metadata_value in metadata_blocks.items():
                if metadata_value['name'] not in all_filter_groups_names:
                    filter_group = FilterGroup.objects.create(
                        name=metadata_value['name'],
                        friendly_name=metadata_value['displayName'] + f'{lang}',
                        language=lang
                    )
                else:
                    filter_group = FilterGroup.objects.get(name=metadata_value['name'],
                                                           language=lang)
                for _, field_data in metadata_value['fields'].items():
                    if field_data['name'] not in al_filter_fields_names:
                        if not field_data['name'] in wrong_names:
                            # TODO: delete on production
                            FilterField.objects.create(
                                field_name=field_data['name'],
                                filter_group=filter_group,
                                public=False
                            )
            all_advanced_search_filter_groups_names = [filter_group['name'] for
                                                       filter_group in
                                                       AdvancedSearchFilterGroup.objects.get_by_lang(
                                                           lang).values(
                                                           'name')]
            al_advanced_search_filter_fields_names = []
            for filter_group in AdvancedSearchFilterGroup.objects.get_by_lang(lang):
                al_advanced_search_filter_fields_names += [filter_field['field_name'] for
                                                           filter_field in
                                                           filter_group.fields.all().values(
                                                               'field_name')]

            for metadata_name, metadata_value in metadata_blocks.items():
                if metadata_value['name'] not in all_advanced_search_filter_groups_names:
                    filter_group = AdvancedSearchFilterGroup.objects.create(
                        name=metadata_value['name'],
                        friendly_name=metadata_value['displayName'] + f'{lang}',
                        language=lang
                    )
                else:
                    filter_group = AdvancedSearchFilterGroup.objects.get(
                        name=metadata_value['name'], language=lang)
                for _, field_data in metadata_value['fields'].items():
                    if field_data['name'] not in al_advanced_search_filter_fields_names:
                        AdvancedSearchFilterField.objects.create(
                            field_name=field_data['name'],
                            friendly_name=field_data['displayName'],
                            title=field_data['title'],
                            type=field_data['type'],
                            description=field_data['description'],
                            filter_group=filter_group,
                        )
        return True

    @staticmethod
    def populate_categories(categories_jsonized: str) -> bool:
        """
        Method responsible for updating all categories -
        it must only add new categories with default public status to false
        :param categories_jsonized: jsonized categories list
        :return: True if success
        """
        successfully_populated = False
        try:
            categories = json.loads(categories_jsonized)
            agregator_categories_names = [category['name'] for category in
                                          AgregatorCategory.objects.all().values('name')]
            for category in categories['categories']:
                if category['name'] not in agregator_categories_names:
                    for lang in LANGUAGES:
                        AgregatorCategory.objects.create(dataverse_id=category['id'],
                                                         friendly_name=category[
                                                                           'friendly_name'] + f" | {lang[0]}",
                                                         name=category['name'],
                                                         description=category[
                                                             'description'],
                                                         dv_affiliation=category[
                                                             'dvAffiliation'],
                                                         dv_name=category['dvName'],
                                                         publication_date=category[
                                                             'publicationDate'],
                                                         language=lang[0])
            successfully_populated = True
        except Exception as ex:
            print(ex)
        return successfully_populated
