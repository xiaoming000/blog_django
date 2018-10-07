from django.conf.urls import url
from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^python/$', views.python_list, name='python_list'),
    url(r'^linux/$', views.linux_list, name='linux_list'),
    url(r'^other/$', views.other_list, name='other_list'),
    url(r'^essay/$', views.essay_list, name='essay_list'),
    url(r'^message/$', views.message, name='message'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^push/$', views.push, name='push'),
    url(r'^add_tags/$', views.add_tags, name='add_tags'),
    url(r'^del_comment/$', views.del_comment, name='del_comment'),
    url(r'^del_reply/$', views.del_reply, name='del_reply'),
]