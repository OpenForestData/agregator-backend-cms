# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from blog.views import detail, index, keyword, latest

app_name = 'blog'

urlpatterns = [
    # /cms-api/v1/blog/article/slug-of-the-article
    url(r'^article/(?P<slug>[\w\-]+)$', detail, name="detail"),
    # /cms-api/v1/blog/keyword/slug-of-the-keyword
    url(r'^keyword/(?P<slug>[\w\-]+)$', keyword, name="keyword"),
    # /cms-api/v1/blog/index
    url(r'^index$', index, name="index"),
    # /cms-api/v1/blog/latest
    url(r'^latest$', latest, name="latest"),
]
