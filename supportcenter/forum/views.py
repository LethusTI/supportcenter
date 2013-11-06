# -*- coding: utf-8 -*-

__all__ = (
    'ListForumView', 'AddForumView',
    'DetailForumView', 'DeleteForumView',
    'DeleteReplyView')

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
        queryset = self.document.objects.order_by(
            '-date')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(comment__icontains=search)
            )
        
        return queryset
    

class ForumViewMixIn(object):
    document = Forum
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

    def get_success_url(self):
        return self.object.get_absolute_url()
        
class DetailForumView(CreateView):
    template_name = 'forum/detail.html'
    success_message = _("Your reply has been added")

    def get_form_class(self):
        return AddReplyForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_forum(self, *args, **kwargs):
        id = self.kwargs.get('id')
        object = get_document_or_404(
            Forum,
            id=int(id),
        )
        return object


    def get_context_data(self, *args, **kwargs):
        ctx = super(DetailForumView, self).get_context_data(*args, **kwargs)
        ctx['object'] = self.get_forum()
        return ctx

    def get_form_kwargs(self, *args, **kwargs):
        fw = super(DetailForumView, self).get_form_kwargs(*args, **kwargs)
        fw['user'] = self.request.user
        fw['forum'] = self.get_forum()
        
        return fw


class DeleteForumView(DeleteView):
    document = Forum
    template_name = 'forum/confirm_delete.html'
    success_url = '/forum/'
    success_message = _(u"The topic has been destroyed")
    
    def get_object(self, *args, **kwargs):
        return get_document_or_404(
            Forum,
            id=int(self.kwargs['id'])
        )

class DeleteReplyView(DeleteView):
    document = Reply
    template_name = 'forum/confirm_delete_reply.html'
    success_url = '/forum/'
    success_message = _(u"The topic has been destroyed")
    
    def get_object(self, *args, **kwargs):
        return get_document_or_404(
            Reply,
            id=int(self.kwargs['id'])
        )
