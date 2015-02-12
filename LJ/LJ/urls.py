from django.conf.urls import patterns, include, url
from django.conf import settings
from LJblog.views import PostListView

urlpatterns = patterns('',
	url(r'^$', PostListView.as_view(), name='list'),
    url(r'^post/', include('LJblog.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   
    # url(r'^(?P<post_id>[\w\d]+)/add_comments/$', 'LJblog.views.add_comments', name='add_comments'),
)


