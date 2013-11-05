# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from supportcenter.accounts.decorators import superuser_only

from supportcenter.accounts.views import (
    ListSuperUserView, AddSuperUserView, UpdateSuperUserView,
    SetPasswordSuperUserView,
    AccountSettingView, AccountSetPasswordView)

from .views import AdminSettingsView, SuperMainView
from supportcenter.faq.views import (
    ListCategoryView, AddCategoryView, UpdateCategoryView,
    ListQuestionAdminView, AddQuestionAdminView,
    UpdateQuestionAdminView)

urlpatterns = patterns(
    '',
    url(r'^add/$', superuser_only(AddQuestionAdminView.as_view())),
    url(r'^(?P<pk>\d+)/$', superuser_only(UpdateQuestionAdminView.as_view())),

    url(r'^categories/$', superuser_only(ListCategoryView.as_view())),
    url(r'^categories/add/$', superuser_only(AddCategoryView.as_view())),
    url(r'^categories/(?P<pk>\w{24})/$', superuser_only(UpdateCategoryView.as_view())),
    
    url(r'^superusers/$', superuser_only(ListSuperUserView.as_view())),
    url(r'^superusers/add/$', superuser_only(AddSuperUserView.as_view())),
    url(r'^superusers/(?P<pk>\w{24})/$', superuser_only(UpdateSuperUserView.as_view())),
    url(r'^superusers/(?P<pk>\w{24})/password/$', superuser_only(SetPasswordSuperUserView.as_view())),
    
    url('^settings/$', superuser_only(AdminSettingsView.as_view())), 
)
