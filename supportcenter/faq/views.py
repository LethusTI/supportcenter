# -*- coding: utf-8 -*-

__all__ = (
    'FaqIndexView', 'ListQuestionView',
    'AddQuestionAdminView',
    'UpdateQuestionAdminView',
    'ListCategoryView', 'AddCategoryView',
    'UpdateCategoryView')

from mongotools.views import (
    ListView, CreateView, UpdateView)
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
    pass

class AddQuestionView(IncludeCategoriesTemplate, CreateView):
    document = Question
    form_class = AddQuestionForm
    template_name = 'faq/ask.html'
    
    def get_form_kwargs(self, *args, **kwargs):
        fw = super(AddQuestionView, self).get_form_kwargs(*args, **kwargs)
        fw['user'] = self.request.user
        
        return fw
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
    
class UpdateQuestionAdminView(QuestionAdminViewMixIn, UpdateView):
    success_message = u"A questão foi atualizada com sucesso"

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
