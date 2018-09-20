from django import forms
from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_type', 'comment', 'text']
