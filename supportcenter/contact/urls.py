from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf import settings

from supportcenter.accounts.decorators import superuser_only

from .views import *

urlpatterns = patterns('',
    url(r'^$', AddContactView.as_view(), name="contact"),
    url(r'^sent/',ContactView.as_view(), name='contact_sent'),
)
