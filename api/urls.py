from django.conf.urls import url
from django.urls import include

from api import views as api_views

app_name = 'api'

urlpatterns = [
    # /cms-api/v1/facet-list
    url(r'^facet-list$', api_views.facet_list, name="facet_list"),
    # /cms-api/v1/populate-categories-fields-list
    url(r'^populate-categories-fields-list$', api_views.populate_categories_fields_list,
        name="populate_categories_fields_list"),
    # /cms-api/v1/register-metadata-blocks
    url(r'^register-metadata-blocks$', api_views.ragister_metadata_blocks, name="ragister_metadata_blocks"),
    # /cms-api/v1/menu
    url(r'^menu$', api_views.menu, name="global_data"),
    # /cms-api/v1/tree-details
    url(r'^tree-details/(?P<page_id>[0-9]+)/(?P<lang_code>[\w-]{2})$', api_views.page_details, name="page_details"),
    # /cms-api/v1/get-categories
    url(r'^get-categories$', api_views.get_categories_fields_list, name="get_categories_fields_list"),
    # /cms-api/v1/faq
    url(r'^faq$', api_views.get_faq, name="get_faq"),
    # /cms-api/v1/news
    url(r'^news/', include('news.urls', namespace='news')),
    # /cms-api/v1/blog
    url(r'^blog/', include('blog.urls', namespace='blog')),
    # /cms-api/v1/home
    url(r'^home$', api_views.home, name='home'),
]
