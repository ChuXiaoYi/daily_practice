#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/19 下午2:43
# @Author  : cxy
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @desc    :
from django.conf.urls import url
from . import views
app_name = 'blog'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archive, name='archive'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
]