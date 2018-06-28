#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 上午9:36
# @Author  : cxy
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @desc    :
from django.conf.urls import url
from . import views
app_name = 'block_app'

urlpatterns = [
    url(r'mine/$', views.mine, name='mine'),
    url(r'transactions/new/$', views.new_transaction, name='new_transaction'),
    url(r'chain/$', views.full_chain, name='full_chain'),
    # url(r'register/$', views.register_nodes),
]