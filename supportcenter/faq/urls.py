from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .views import *

urlpatterns = patterns(
    '',
    url(r'^$', FaqIndexView.as_view(), name="knowledge_index"),
)
