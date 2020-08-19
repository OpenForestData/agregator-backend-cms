# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from news.views import detail, latest

app_name = 'news'

urlpatterns = [
    # /pl/cms-api/v1/news/slug-for-the-news
    url(r'^(?P<slug>[\w\-]+)$', detail, name="detail"),
    # /pl/cms-api/v1/news/latest
    url(r'^latest$', latest, name="latest"),
]
