from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf import settings

from supportcenter.accounts.views import (AccountSettingView, AccountSetPasswordView)
from supportcenter.faq.views import (
    FaqIndexView, ListQuestionView, AddQuestionView)

urlpatterns = patterns(
    '',
    url(r'^auth/', include('supportcenter.accounts.urls')),
    
    url(r'^$', FaqIndexView.as_view(), name="knowledge_index"),
    url(r'^questions/$', ListQuestionView.as_view(), name='knowledge_list'),
    url(r'^ask/$', AddQuestionView.as_view(), name='knowledge_ask'),
    
    url(r'^account/$', login_required(AccountSettingView.as_view())),
    url(r'^account/set_password/$',
        login_required(AccountSetPasswordView.as_view())),

    #Admin
    url(r'^admin/', include('supportcenter.admin.urls')),
)
