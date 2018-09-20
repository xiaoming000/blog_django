from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Reply
from .forms import CommentForm, PostReplyForm


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)


def post_reply(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # post_comment = get_object_or_404(PostComent, pk= post_comment_pk)
    user = request.user
    if request.method == "POST":
        reply_form = PostReplyForm(request.POST)
        if reply_form.is_valid():
            reply_form = reply_form.save(commit=False)
            if request.POST['comment_reply']:
                reply_form.comment_reply = Reply.objects.filter(pk=request.POST['comment_reply'])[0]
            reply_form.user = user
            reply_form.save()

            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': CommentForm(),
                'reply_form': reply_form,
                'comment_list': comment_list
            }
        return render(request, 'blog/detail.html', context=context)
    return redirect(post)

