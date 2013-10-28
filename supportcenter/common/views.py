# -*- coding: utf-8 -*-

__all__ = ('PrincipalView',)

from django.views.generic import TemplateView

class PrincipalView(TemplateView):
    template_name = 'principal.html'
