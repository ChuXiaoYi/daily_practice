#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 上午9:32
# @Author  : cxy
# @Site    : 
# @File    : blog_tags.py
# @Software: PyCharm
# @desc    : 自定义模版标签

from ..models import User
from django import template
register = template.Library()


@register.simple_tag
def get_users():
    """
    获取最新的五篇文章模版标签
    将该标签注册到django中，才能使用
    :param num:
    :return:
    """
    return User.objects.all()



