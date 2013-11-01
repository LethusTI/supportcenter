from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .views import *

urlpatterns = patterns(
    '',
        url(r'^$', ListQuestionView.as_view(), name="knowledge_index"),
    url(r'^questions/(?P<pk>\d+)/$',
        DetailQuestionView.as_view(), name='knowledge_thread_no_slug'),
    url(r'^questions/(?P<category_slug>[a-z0-9-_]+)/$', ListQuestionView.as_view(),
        name='knowledge_list_category'),
)
