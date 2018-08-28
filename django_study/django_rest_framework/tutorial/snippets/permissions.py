# -*- coding: utf-8 -*-
# --------------------------------------
#       @Time    : 2018/8/27 下午4:22
#       @Author  : cxy =.= 
#       @File    : permissions.py
#       @Software: PyCharm
# --------------------------------------
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """保证只有所属者可以更新删除该snippet"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
