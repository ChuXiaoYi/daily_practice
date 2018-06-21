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
app_name = 'comments'

urlpatterns = [
    url(r'comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment')
]