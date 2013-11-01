# -*- coding: utf-8 -*-

__all__ = (
    'IndexView',)


from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'
