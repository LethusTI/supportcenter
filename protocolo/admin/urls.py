# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from protocolo.accounts.decorators import superuser_only

from protocolo.accounts.views import (
    ListSuperUserView, AddSuperUserView, UpdateSuperUserView,
    SetPasswordSuperUserView, ListUnidadeProfileView,
    AddUnidadeProfileView, UpdateUnidadeProfileView,
    SetPasswordUnidadeProfileView, HistoricSuperUserView,
    HistoricUnidadeProfileView, GeneralHistoricView,
    AccountSettingView, AccountSetPasswordView)

from views import AdminSettingsView


urlpatterns = patterns('',
    url(r'^superusers/$', superuser_only(ListSuperUserView.as_view())),
    url(r'^superusers/add/$', superuser_only(AddSuperUserView.as_view())),
    url(r'^superusers/(?P<pk>\w{24})/$', superuser_only(UpdateSuperUserView.as_view())),
    url(r'^superusers/(?P<pk>\w{24})/password/$', superuser_only(SetPasswordSuperUserView.as_view())),
    url(r'^superusers/logs/(?P<pk>\w{24})/$', superuser_only(HistoricSuperUserView.as_view())),

    url(r'^users/$', superuser_only(ListUnidadeProfileView.as_view())),
    url(r'^users/add/$', superuser_only(AddUnidadeProfileView.as_view())),
    url(r'^users/(?P<pk>\w{24})/$', superuser_only(UpdateUnidadeProfileView.as_view())),
    url(r'^users/(?P<pk>\w{24})/password/$', superuser_only(SetPasswordUnidadeProfileView.as_view())),
    url(r'^users/logs/(?P<pk>\w{24})/$', superuser_only(HistoricUnidadeProfileView.as_view())),

    url(r'^logs/',superuser_only(GeneralHistoricView.as_view())),
    
    url('^settings/$', superuser_only(AdminSettingsView.as_view())),

    url(r'^unidades/', include("protocolo.unidades.urls")),
 
)
