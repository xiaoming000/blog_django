from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from comments.forms import CommentForm
from comments.models import Comment, Reply
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from .form import PostForm
from .models import Post, Category, Tag
import markdown
import json
import datetime


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data( **kwargs)
        context.update({
            'htitle': "首页-梦flying的博客"
        })
        return context

    # 分页

    # def get_context_data(self, **kwargs):
    #     """
    #     在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
    #     例如 render(request, 'blog/index.html', context={'post_list': post_list})，
    #     这里传递了一个 {'post_list': post_list} 字典给模板。
    #     在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
    #     所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
    #     """
    #
    #     # 首先获得父类生成的传递给模板的字典。
    #     context = super().get_context_data(**kwargs)
    #
    #     # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
    #     # paginator 是 Paginator 的一个实例，
    #     # page_obj 是 Page 的一个实例，
    #     # is_paginated 是一个布尔变量，用于指示是否已分页。
    #     # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
    #     # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
    #     # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
    #     paginator = context.get('paginator')
    #     page = context.get('page_obj')
    #     is_paginated = context.get('is_paginated')
    #
    #     # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
    #     pagination_data = self.pagination_data(paginator, page, is_paginated)
    #
    #     # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
    #     context.update(pagination_data)
    #
    #     # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
    #     # 注意此时 context 字典中已有了显示分页导航条所需的数据。
    #     return context

    # def pagination_data(self, paginator, page, is_paginated):
    #     if not is_paginated:
    #         # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
    #         return {}
    #
    #     # 当前页左边连续的页码号，初始值为空
    #     left = []
    #
    #     # 当前页右边连续的页码号，初始值为空
    #     right = []
    #
    #     # 标示第 1 页页码后是否需要显示省略号
    #     left_has_more = False
    #
    #     # 标示最后一页页码前是否需要显示省略号
    #     right_has_more = False
    #
    #     # 标示是否需要显示第 1 页的页码号。
    #     # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
    #     # 其它情况下第一页的页码是始终需要显示的。
    #     # 初始值为 False
    #     first = False
    #
    #     # 标示是否需要显示最后一页的页码号。
    #     # 需要此指示变量的理由和上面相同。
    #     last = False
    #
    #     # 获得用户当前请求的页码号
    #     page_number = page.number
    #
    #     # 获得分页后的总页数
    #     total_pages = paginator.num_pages
    #
    #     # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
    #     page_range = paginator.page_range
    #
    #     if page_number == 1:
    #         # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
    #         # 此时只要获取当前页右边的连续页码号，
    #         # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
    #         # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
    #         right = page_range[page_number:page_number + 2]
    #
    #         # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
    #         # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
    #         if right[-1] < total_pages - 1:
    #             right_has_more = True
    #
    #         # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
    #         # 所以需要显示最后一页的页码号，通过 last 来指示
    #         if right[-1] < total_pages:
    #             last = True
    #
    #     elif page_number == total_pages:
    #         # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
    #         # 此时只要获取当前页左边的连续页码号。
    #         # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
    #         # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
    #         left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
    #
    #         # 如果最左边的页码号比第 2 页页码号还大，
    #         # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
    #         if left[0] > 2:
    #             left_has_more = True
    #
    #         # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
    #         # 所以需要显示第一页的页码号，通过 first 来指示
    #         if left[0] > 1:
    #             first = True
    #     else:
    #         # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
    #         # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
    #         left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
    #         right = page_range[page_number:page_number + 2]
    #
    #         # 是否需要显示最后一页和最后一页前的省略号
    #         if right[-1] < total_pages - 1:
    #             right_has_more = True
    #         if right[-1] < total_pages:
    #             last = True
    #
    #         # 是否需要显示第 1 页和第 1 页后的省略号
    #         if left[0] > 2:
    #             left_has_more = True
    #         if left[0] > 1:
    #             first = True
    #
    #     data = {
    #         'left': left,
    #         'right': right,
    #         'left_has_more': left_has_more,
    #         'right_has_more': right_has_more,
    #         'first': first,
    #         'last': last,
    #     }
    #
    #     return data


def python_list(request):
    category = Category.objects.get(name='Python')
    post = Post.objects.filter(category_id=category)
    context = {
        'python_list': post,
        'htitle': "Python-梦flying的博客",
    }
    return render(request, 'blog/python.html', context=context)


def linux_list(request):
    category = Category.objects.get(name='Linux')
    post = Post.objects.filter(category_id=category)
    context = {
        'linux_list': post,
        'htitle': "Linux-梦flying的博客",
        'nav': 2,
    }
    return render(request, 'blog/Linux.html', context=context)


def other_list(request):
    category = Category.objects.get(name='Other')
    post = Post.objects.filter(category_id=category)
    context = {
        'other_list': post,
        'htitle': "其他技术文章-梦flying的博客",
        'nav': 3,
    }
    return render(request, 'blog/other.html', context=context)


def essay_list(request):
    category = Category.objects.get(name='Essay')
    post = Post.objects.filter(category_id=category)
    context = {
        'essay_list': post,
        'htitle': "随笔-梦flying的博客",
    }
    return render(request, 'blog/essay.html', context=context)


def message(request):
    context = {
        'htitle': "与我联系-梦flying的博客",
    }
    return render(request, 'blog/message.html', context=context)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchivesView(IndexView):
    def get_queryset(self):
        # year = get_object_or_404(Category, pk=self.kwargs.get('year'))
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify, baselevel=2),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        # if len(post.toc) == 0:
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


@login_required()
def push(request):
    if request.method == 'POST'and request.user.is_staff:
        form = PostForm(request.POST)
        if form.is_valid():
            tags = request.POST.getlist('tags[]')
            # return HttpResponse(tags)
            post = form.save(commit=False)
            post.author = request.user
            post.created_time = datetime.datetime.now()
            post.modified_time = datetime.datetime.now()
            post.save()
            post.tags.set(tags)
            return redirect('/')
    else:
        form = PostForm()
        context = {
            'form': form,
        }
    return render(request, 'blog/push.html', context=context)


@login_required()
def add_tags(request):
    if request.method == 'POST' and request.user.is_staff:
        tags = request.POST.get('tags', '')
        tags_list = tags.split()
        response = {}
        for tag in tags_list:
            try:
                tag_obj = Tag()
                tag_obj.name = tag
                tag_obj.save()
                response[tag] = "添加成功！"
            except IntegrityError:
                response[tag] = "添加失败！"
        return HttpResponse(json.dumps({'response': response}), content_type="application/json")

    return HttpResponse(json.dumps({'response': "请求错误！"}), content_type="application/json")


# 删除操作
@login_required()
def del_comment(request):
    if request.method == 'POST' and request.user.is_staff:
        comment_id = request.POST.get('comment_id', '')
        try:
            Comment.objects.filter(pk=comment_id).delete()
            response = "删除成功！"
        except BaseException:
            response = "删除失败！"

        return HttpResponse(json.dumps(response), content_type="application/json")


# 删除操作
@login_required()
def del_reply(request):
    if request.method == 'POST' and request.user.is_staff:
        reply_id = request.POST.get('reply_id', '')
        try:
            Reply.objects.filter(pk=reply_id).delete()
            response = "删除成功！"
        except BaseException:
            response = "删除失败！"

        return HttpResponse(json.dumps(response), content_type="application/json")