# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from news.views import detail, latest

app_name = 'news'

urlpatterns = [
    url(r'^news/(?P<slug>[\w\-]+)$', detail, name="detail"),
    url(r'^latest$', latest, name="latest"),
]
