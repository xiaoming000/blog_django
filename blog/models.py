from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)  # 分类名

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)  # 标签名

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)  # 文章标题
    body = models.TextField()  # 文章正文
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)  # 文章摘要
    category = models.ForeignKey(Category)  # 文章分类
    tags = models.ManyToManyField(Tag, blank=True)  # 文章标签
    author = models.ForeignKey(User)  # 文章作者
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-created_time']