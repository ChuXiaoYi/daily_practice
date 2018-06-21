from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown

class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_category_url(self):
        """
        获取category的url
        :return:
        """
        return reverse('blog:category', kwargs={'pk': self.id})


class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """文章"""
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)  # 文章摘要，可为空
    category = models.ForeignKey(Category, on_delete=True)  # ForeignKey表示1对多（多个post对应1个category）
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, on_delete=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        用于自动生成摘要
        :return:
        """
        if not self.excerpt:
            # 如果没有摘要
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)

    def increase_views(self):
        """
        增加阅读量
        :return:
        """
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        """
        自定义 get_absolute_url 方法,反向解析url
        :return:
        """
        return reverse('blog:detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-created_time']
