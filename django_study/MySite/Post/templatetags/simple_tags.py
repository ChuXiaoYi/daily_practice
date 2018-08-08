# -*- coding: utf-8 -*-
# --------------------------------------
#       @Time    : 2018/8/8 上午10:45
#       @Author  : cxy =.= 
#       @File    : simple_tags.py
#       @Software: PyCharm
# --------------------------------------
from django import template
from ..models import Category
from comment.models import Comment

register = template.Library()


@register.simple_tag
def get_categories():
    """
    分类目录标签
    :return:
    """
    return Category.objects.all()


@register.simple_tag
def get_latest_comment():
    """
    获取最新评论
    :return:
    """
    comment_list = Comment.objects.all()[:5].only('post', 'text')   # 只获取特定字段
    return comment_list
