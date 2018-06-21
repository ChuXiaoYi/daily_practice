from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            print(comment_list)
            context = {
                "post": post,
                "form": form,
                "comment_list": comment_list
            }
            return render(request, 'blog/single.html', context)
    return redirect(post)