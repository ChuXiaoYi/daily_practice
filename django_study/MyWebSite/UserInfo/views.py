from django.shortcuts import render
from .models import User


def index(request):
    """
    主页
    需要向前端渲染用户
    :param request:
    :return:
    """
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'index.html', context=context)
