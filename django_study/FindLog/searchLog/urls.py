#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 下午4:45
# @Author  : cxy
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @desc    :
from django.conf.urls import url
from . import views

app_name = 'searchLog'

urlpatterns = [
    url(r'index/$', views.index, name='index'),
    url(r'search_log/$', views.search_log, name='search_log')
]