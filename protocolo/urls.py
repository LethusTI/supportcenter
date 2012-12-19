from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf import settings

from protocolo.common.views import PrincipalView
from protocolo.accounts.views import (AccountSettingView, AccountSetPasswordView)

urlpatterns = patterns(
    '',
    url(r'^auth/', include('protocolo.accounts.urls')),
    url(r'^$', login_required(PrincipalView.as_view())),
    url(r'image_constant/(?P<key>.*)$',
        'protocolo.admin.views.image_constant', name='image_constant'),

    url(r'^account/$', login_required(AccountSettingView.as_view())),
    url(r'^account/set_password/$',
        login_required(AccountSetPasswordView.as_view())),

    #Admin
    url(r'^admin/', include('protocolo.admin.urls')),


)
