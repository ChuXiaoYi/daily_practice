# -*- coding: utf-8 -*-
# --------------------------------------
#       @Time    : 2018/8/24 下午4:51
#       @Author  : cxy =.= 
#       @File    : urls.py
#       @Software: PyCharm
# --------------------------------------
from django.conf.urls import url
from . import views
app_name = 'snippets'

urlpatterns = [
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail)
]