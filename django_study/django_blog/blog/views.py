from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown


def index(request):
    """
    首页
    :param request:
    :return:
    """
    post_list = Post.objects.all()
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context=context)


def detail(request, pk=0):
    """
    详情页
    :param request:
    :return:
    """
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc'
                                  ])
    context = {
        'post': post,
        'comment_list': post.comment_set.all()
    }
    return render(request, 'blog/single.html', context=context)


def archive(request, year, month):
    """
    通过归档查询文章
    :param request:
    :param year:
    :param month:
    :return:
    """
    post_list = Post.objects.filter(created_time__year=year,
                                    # created_time__month=month
                                    )
    print(post_list)
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context=context)


def category(request, pk=1):
    """
    通过目录查询文章
    :param request:
    :param pk:
    :return:
    """
    post_list = Post.objects.filter(category=pk)
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context=context)