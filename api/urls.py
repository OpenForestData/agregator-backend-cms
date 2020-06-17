from django.conf.urls import url

from api import views as api_views

app_name = 'api'

urlpatterns = [
    # /api/v1/facet-list
    url(r'^facet-list$', api_views.facet_list, name="facet_list"),
    # /api/v1/populate-categories-fields-list
    url(r'^populate-categories-fields-list$', api_views.populate_categories_fields_list,
        name="populate_categories_fields_list"),
    # /api/v1/register-metadata-blocks
    url(r'^register-metadata-blocks$', api_views.ragister_metadata_blocks, name="ragister_metadata_blocks"),
    # /api/v1/global-data
    url(r'^global-data$', api_views.global_data, name="global_data"),
    # /api/v1/get-categories-fields-list
    url(r'^get-categories$', api_views.get_categories_fields_list, name="get_categories_fields_list")
]
