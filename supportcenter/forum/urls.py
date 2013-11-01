from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .views import *

urlpatterns = patterns('',
    url(r'^$', ListForumView.as_view(), name="forum"),
    url(r'^add/',AddForumView.as_view(), name='add_forum'),
    url(r'^update/(?P<id>\d+)/', DetailForumView.as_view(),
        name='update_forum'),
    url(r'^admin/$', ListForumView.as_view(), name="forum_admin"),
    url(r'^admin/update/(?P<id>\d+)/', DetailAdminForumView.as_view(), name="update_forum_admin"),
    url(r'^admin/delete/(?P<id>\d+)/', DeleteAdminForumView.as_view(), name="delete_forum_admin"),

)
