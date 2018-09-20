from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):

    text = models.TextField()
    delete = models.SmallIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]


class Reply(models.Model):
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    delete = models.SmallIntegerField(default=0)
    reply_type = models.SmallIntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    comment_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text[0:20]
