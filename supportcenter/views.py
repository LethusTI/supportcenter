# -*- coding: utf-8 -*-

__all__ = (
    'IndexView',)

from django.views.generic import TemplateView
from supportcenter.faq.models import Question
from supportcenter.forum.models import Forum

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(IndexView, self).get_context_data(*args, **kwargs)
        ctx['last_questions'] = Question.objects.order_by('-added')[0:5]
        ctx['last_forum'] = Forum.objects.order_by('-date')[0:5]
        
        return ctx
