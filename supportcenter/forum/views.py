# -*- coding: utf-8 -*-

__all__ = (
    'ListForumView', 'AddForumView',
    'DetailForumView', 'ListAdminForumView',
    'DetailAdminForumView', 'DeleteAdminForumView')

from mongotools.views import (
    ListView, CreateView, UpdateView, 
    DetailView, DeleteView)
from mongoengine.queryset import Q
from mongoengine.django.shortcuts import get_document_or_404
from django.utils.translation import ugettext_lazy as _
from lethusbox.django.responses import HybridListView

from .models import *
from .forms import *

class ListForumView(ListView):
    document = Forum
    template_name = 'forum/list.html'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        ctx = super(ListForumView, self).get_context_data(*args, **kwargs)

        search = self.request.GET.get('title', None)
        
        ctx['search'] = search
        
        return ctx

    def get_queryset(self):
        search = self.request.GET.get('title', None)
        queryset = self.document.objects

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(comment__icontains=search)
            )
        
        return queryset
    

class ForumViewMixIn(object):
    document = Forum
    form_class = AddForumForm
    success_url = '/forum/'

    def get_form_class(self, *args, **kwargs):
        return AddForumForm
    
    def get_form_kwargs(self, *args, **kwargs):
        fw = super(ForumViewMixIn, self).get_form_kwargs(*args, **kwargs)
        fw['user'] = self.request.user
        return fw

class AddForumView(ForumViewMixIn, CreateView):
    template_name = 'forum/form.html'
    success_message = _("Your question has been added")

class DetailForumView(CreateView):
    template_name = 'forum/detail.html'
    form_class = AddReplyForm 
    success_url = '/forum/update/%d/'
    success_message = _("Your reply has been added")

    def get_success_url(self):
        forum = self.get_forum()
        return "/forum/update/%d/" % forum.id

    def get_forum(self, *args, **kwargs):
        id = self.kwargs.get('id')
        object = get_document_or_404(
            Forum,
            id=int(id),
        )
        return object

    def get_reply(self, *args, **kwargs):
        object = get_document_or_404(
            Reply,
        )
        return object

    def get_context_data(self, *args, **kwargs):
        ctx = super(DetailForumView, self).get_context_data(*args, **kwargs)
        ctx['object'] = self.get_forum()
        ctx['replys'] = self.get_reply()
        return ctx

    def get_form_kwargs(self, *args, **kwargs):
        fw = super(DetailForumView, self).get_form_kwargs(*args, **kwargs)
        fw['user'] = self.request.user
        
        return fw


class ListAdminForumView(HybridListView):
    document = Forum
    template_name = 'forum/list_admin.html'
    paginate_by = 20
    allow_empty = True
    json_object_list_fields = ['id', 'title', 'name']
    filter_fields = ['title']

class DetailAdminForumView(UpdateView):
    document = Forum
    template_name = 'forum/detail_admin.html'

class DeleteAdminForumView(DeleteView):
    document = Forum
    template_name = 'forum/delete_admin.html'
