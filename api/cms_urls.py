# -*- coding: utf-8 -*-
from cms import views
from cms.apphook_pool import apphook_pool
from cms.appresolver import get_app_patterns
from cms.constants import SLUG_REGEXP
from django.conf import settings
from django.conf.urls import include, url
from api import views as api_views

if settings.APPEND_SLASH:
    regexp = r'^(?P<slug>%s)/$' % SLUG_REGEXP
else:
    regexp = r'^(?P<slug>%s)$' % SLUG_REGEXP

if apphook_pool.get_apphooks():
    urlpatterns = get_app_patterns()
else:
    urlpatterns = []

urlpatterns.extend([
    url(r'^cms_login/$', views.login, name='cms_login'),
    url(r'^cms_wizard/', include('cms.wizards.urls')),
    url(regexp, api_views.page_details, name='pages-details-by-slug'),
    url(r'^$', api_views.page_details, {'slug': ''}, name='pages-root'),
])
