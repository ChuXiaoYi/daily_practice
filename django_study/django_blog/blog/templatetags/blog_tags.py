#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/20 上午9:32
# @Author  : cxy
# @Site    : 
# @File    : blog_tags.py
# @Software: PyCharm
# @desc    : 自定义模版标签

from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count
register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    """
    获取最新的五篇文章模版标签
    将该标签注册到django中，才能使用
    :param num:
    :return:
    """
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    """
    归档模版标签
    created_time：Post 的创建时间
    month：精度
    order='DESC'：表明降序排列（即离当前越近的时间越排在前面）
    :return:
    """
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """
    分类模版标签
    :return:
    """
    # return Category.objects.all()
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    """
    获取标签的模版标签
    :return:
    """
    return Tag.objects.all()
