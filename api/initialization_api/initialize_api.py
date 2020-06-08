from api.models import FacetField

START_FACET_FIELDS = [
    {'field_name': 'publicationDate', 'friendly_name': "Data publikacji", "order": 1},

    {'field_name': 'language', 'friendly_name': "Język", "order": 2},

    {'field_name': 'isHarvested', 'friendly_name': "Pochodzi od harvestera", "order": 3}
]


def initialize_facet_fields():
    print('Starting adding facet fields')
    for field in START_FACET_FIELDS:
        FacetField(
            facet_field_name=field['field_name'],
            facet_field_friendly_name=field['friendly_name'],
            order=field['order']
        ).save()
    print(f'End adding facet fields, amount: {len(FacetField.objects.all())}')


def initialize_api():
    initialize_facet_fields()
