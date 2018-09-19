import markdown
from django.utils.html import strip_tags
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 文章分类
    tags = models.ManyToManyField(Tag, blank=True)  # 文章标签
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 文章作者
    views = models.PositiveIntegerField(default=0)  # 阅读量

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = '    '+strip_tags(md.convert(self.body))[:80]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']