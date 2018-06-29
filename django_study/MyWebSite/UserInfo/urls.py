#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/28 上午11:45
# @Author  : cxy
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @desc    :
from django.conf.urls import url
from . import views
from MyWebSite.settings import MEDIA_ROOT
from django.views.static import serve

app_name = 'UserInfo'

urlpatterns = [
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'index/$', views.index, name='index')
]
