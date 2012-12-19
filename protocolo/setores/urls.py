# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from protocolo.accounts.decorators import superuser_only

from views import AddSetorView, EditSetorView, ListSetorView

urlpatterns = patterns('',
    url(r'^$',
        superuser_only(ListSetorView.as_view())),
    url(r'^add/',
        superuser_only(AddSetorView.as_view())),
    url(r'^update/(?P<pk>\w{24})/',
        superuser_only(EditSetorView.as_view())),
)
