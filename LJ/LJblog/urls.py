from django.conf.urls import *
from LJblog import views
from views import PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, AddComment


urlpatterns = patterns('',
    url(r'^add/$', PostCreateView.as_view(), name='create'),
    url(r'^blog_search/$', views.blog_search, name='search'),
    url(r'^(?P<pk>[\w\d]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[\w\d]+)/edit/$', PostUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[\w\d]+)/delete/$', PostDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>[\w\d]+)/add_comments/$', AddComment.as_view(), name='comment'),

    
)

