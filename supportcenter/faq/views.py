# -*- coding: utf-8 -*-

__all__ = (
    'FaqIndexView', 'ListQuestionView',
    'AddQuestionAdminView',
    'UpdateQuestionAdminView',
    'ListCategoryView', 'AddCategoryView',
    'UpdateCategoryView', 'DetailQuestionView')

from mongotools.views import (
    ListView, CreateView, UpdateView, DetailView)
from mongoengine.queryset import Q
from mongoengine.django.shortcuts import get_document_or_404
from django.utils.translation import ugettext_lazy as _
from lethusbox.django.responses import HybridListView

from .models import *
from .forms import *

class IncludeCategoriesTemplate(object):
    def get_context_data(self, *args, **kwargs):
        ctx  = super(IncludeCategoriesTemplate, self).get_context_data(
            *args, **kwargs)

        ctx['categories'] = Category.objects
        
        return ctx
    
class FaqIndexView(IncludeCategoriesTemplate, ListView):
    template_name = 'faq/index.html'

    def get_queryset(self):
        return Question.objects.can_view(
            self.request.user)[0:20]

class ListQuestionView(IncludeCategoriesTemplate, ListView):
    paginate_by = 50
    template_name = 'faq/list.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(ListQuestionView, self).get_context_data(*args, **kwargs)

        search = self.request.GET.get('title', None)
        
        ctx['search'] = search
        ctx['category'] = self.get_category()
        
        ctx['form'] = AddQuestionForm(
            user=self.request.user, initial={'title': search})
        
        return ctx

    def get_category(self):
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            return get_document_or_404(
                Category,
                slug=category_slug)

    def get_queryset(self):
        search = self.request.GET.get('title', None)
        queryset = Question.objects.can_view(
            self.request.user)

        category = self.get_category()
        if category:
            queryset = queryset.filter(
                categories=category)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
        
        return queryset
    
class AddQuestionView(IncludeCategoriesTemplate, CreateView):
    document = Question
    template_name = 'faq/ask.html'
    success_url = '/'
    success_message = _("Your question has been added")

    def get_form_class(self, *args, **kwargs):
        return AddQuestionForm
    
    def get_form_kwargs(self, *args, **kwargs):
        fw = super(AddQuestionView, self).get_form_kwargs(*args, **kwargs)
        fw['user'] = self.request.user
        
        return fw

class DetailQuestionView(IncludeCategoriesTemplate, DetailView):
    document = Question
    template_name = "faq/thread.html"
    def get_object(self):
        return get_document_or_404(
            self.document.objects.can_view(self.request.user),
            pk=int(self.kwargs['pk']))
    
class ListQuestionAdminView(HybridListView):
    document = Question
    template_name = 'faq/admin_list.html'
    paginate_by = 20
    allow_empty = True
    json_object_list_fields = ['id', 'title', 'get_status_display', 'get_categories_display']
    filter_fields = ['title']


class QuestionAdminViewMixIn(object):
    document = Question
    form_class = AdminQuestionForm
    template_name = 'faq/admin_form.html'
    success_url = '/admin/'

    def get_form_kwargs(self, *args, **kwargs):
        fw = super(QuestionAdminViewMixIn, self).get_form_kwargs(*args, **kwargs)
        fw['user'] = self.request.user
        
        return fw
    
class AddQuestionAdminView(QuestionAdminViewMixIn, CreateView):
    success_message = u"A questão foi adicionada com sucesso"
    success_url = '/admin/'
    
class UpdateQuestionAdminView(QuestionAdminViewMixIn, UpdateView):
    success_message = u"A questão foi atualizada com sucesso"
    success_url = '/admin/'
    
    def get_object(self):
        return get_document_or_404(
            self.document,
            pk=int(self.kwargs['pk']))
    
class ListCategoryView(HybridListView):
    document = Category
    template_name = 'faq/category_list.html'
    paginate_by = 20
    allow_empty = True
    json_object_list_fields = ['id', 'title']
    filter_fields = ['title']

class CategoryMixIn(object):
    document = Category
    form_class = CategoryForm
    template_name = 'faq/category_form.html'
    success_url = '/admin/categories/'
    
class AddCategoryView(CategoryMixIn, CreateView):
    pass

class UpdateCategoryView(CategoryMixIn, UpdateView):
    pass
