# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from protocolo.accounts.decorators import superuser_only
from views import *

urlpatterns = patterns('',       
	url(r'^$', superuser_only(ListUnidadeView.as_view())),	
	url(r'^add/$', superuser_only(AddUnidadeView.as_view())),
	url(r'^update/(?P<pk>\w{24})/', superuser_only(UpdateUnidadeView.as_view())),
)
