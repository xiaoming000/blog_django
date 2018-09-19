from django.conf.urls import url
from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^python/$', views.PythonList, name='python_list'),
    url(r'^linux/$', views.LinuxList, name='linux_list'),
    url(r'^other/$', views.OtherList, name='other_list'),
    url(r'^essay/$', views.EssayList, name='essay_list'),
    url(r'^message/$', views.Message, name='message'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
]