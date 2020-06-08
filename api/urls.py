from django.conf.urls import url

from api import views as api_views

app_name = 'api'

urlpatterns = [
    #/api/v1/facet-list
    url(r'^facet-list$', api_views.facet_list, name="facet_list"),
    #/api/v1/global-data
    url(r'^global-data$', api_views.global_data, name="global_data"),
]
