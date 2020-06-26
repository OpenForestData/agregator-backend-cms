from api.models import FilterGroup, FilterField, AdvancedSearchFilterGroup, AdvancedSearchFilterField

BASIC_FILTERS = [{
    'name': "geospatial", 'friendly_name': "Geo Spatial",
    'fields': [
        {'name': "geographicBoundingBox", 'displayName': "Geographic Bounding Box", 'title': "Geographic Bounding Box",
         'type': "MAP", 'description': "Description"}],
}, {
    'name': "citation", 'friendly_name': "Citation",
    'fields': [
        {'name': "dwcModified", 'displayName': "Date Range Test", 'title': "Date Range Test",
         'type': "DATERANGE", 'description': "Date range Description"},
        {'name': "textInput", 'displayName': "Text test", 'title': "Text Test",
         'type': "TEXT", 'description': "Date range Description"}
    ],
}]


def create_static_basic_filters_fields():
    for basic_filter in BASIC_FILTERS:
        filter_group = FilterGroup.objects.create(
            name=basic_filter['name'],
            friendly_name=basic_filter['friendly_name']
        )
        for field_data in basic_filter['fields']:
            FilterField.objects.create(
                field_name=field_data['name'],
                friendly_name=field_data['displayName'],
                title=field_data['title'],
                type=field_data['type'],
                description=field_data['description'],
                filter_group=filter_group,
                public=True
            )

        filter_group = AdvancedSearchFilterGroup.objects.create(
            name=basic_filter['name'],
            friendly_name=basic_filter['friendly_name']
        )
        for field_data in basic_filter['fields']:
            AdvancedSearchFilterField.objects.create(
                field_name=field_data['name'],
                friendly_name=field_data['displayName'],
                title=field_data['title'],
                type=field_data['type'],
                description=field_data['description'],
                filter_group=filter_group,
                public=True
            )
    return True
