# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from blog.views import detail, index, keyword, latest

app_name = 'blog'

urlpatterns = [
    url(r'^article/(?P<slug>[\w\-]+)$', detail, name="detail"),
    url(r'^keyword/(?P<slug>[\w\-]+)$', keyword, name="keyword"),
    url(r'^index$', index, name="index"),
    url(r'^latest$', latest, name="latest"),
]
