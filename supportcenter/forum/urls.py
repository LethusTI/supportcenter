from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf import settings

from supportcenter.accounts.decorators import superuser_only

from .views import *

urlpatterns = patterns('',
    url(r'^$', ListForumView.as_view(), name="forum"),
    url(r'^add/',AddForumView.as_view(), name='add_forum'),
    url(r'^(?P<id>\d+)/', DetailForumView.as_view(),
        name='detail_forum'),

    url(r'^delete/(?P<id>\d+)/', superuser_only(DeleteForumView.as_view()),
        name='detail_forum'),

    url(r'^reply/(?P<id>\d+)/delete', superuser_only(DeleteReplyView.as_view()),
        name='detail_forum'),

)
