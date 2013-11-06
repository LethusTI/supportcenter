# -*- coding: utf-8 -*-

__all__ = ('AddContactView', 'ContactView')

from django.views.generic import (
    TemplateView, FormView)
from mongoengine.queryset import Q
from mongoengine.django.shortcuts import get_document_or_404
from django.utils.translation import ugettext_lazy as _
from lethusbox.django.responses import HybridListView
from django.contrib import messages

from .forms import *

class AddContactView(FormView):
    form_class = ContactForm
    success_url = '/contact/'
    template_name = 'contact/form.html'
    success_message = _("Your contact has been send")

    def form_valid(self, form, *args, **kwargs):
        form.save()
        messages.success(
            self.request,
            u"Email enviado com sucesso.")

        return super(AddContactView, self).form_valid(form, *args, **kwargs)


class ContactView(TemplateView):
    template_name = 'contact/confirm_contact_sent.html'
    success_url = '/contact/'
    success_message = _(u"The email has been send")
  