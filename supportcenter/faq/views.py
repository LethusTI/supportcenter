# -*- coding: utf-8 -*-

__all__ = ('FaqIndexView', 'ListQuestionView')

from mongotools.views import ListView, CreateView

from .models import *

class FaqIndexView(ListView):
    template_name = 'faq/index.html'

    def get_queryset(self):
        return Question.objects.can_view(
            self.request.user)[0:20]

class ListQuestionView(ListView):
    pass

class AddQuestionView(CreateView):
    pass
