#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lethusbox.django.responses.base import *
from lethusbox.django.responses.list import *
from lethusbox.django.responses.json import *
from lethusbox.django.responses.massaction import MassAction

from django.views.generic.edit import BaseDeleteView, ProcessFormView
from django.views.generic.detail import BaseDetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import TemplateView
from django.forms import ValidationError
from django import forms
from django.contrib import messages

from mongotools.views import (MongoSingleObjectTemplateResponseMixin,
                              MongoSingleObjectMixin)

class HFormView(MongoSingleObjectTemplateResponseMixin,
                FormView, MongoSingleObjectMixin):

    close_dialog = False

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an interable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            #if hasattr(queryset, '_clone'):
            #    queryset = queryset._clone()
        elif self.document is not None:
            queryset = self.document.objects
        else:
            raise ImproperlyConfigured(u"'%s' must define 'queryset' or 'document'"
                                       % self.__class__.__name__)
        return queryset

    def get_form(self, form_class):
        """
        Hack para direcionar para o alterador de senha
        """
        user = self.get_object()
        return form_class(user, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = kwargs
        if self.object:
            context['object'] = self.object
        return context

    def render_to_response(self, context):
        context['request'] = self.request

        if hasattr(self, "get_extra_context"):
            context.update(self.get_extra_context())

        return FormView.render_to_response(self,
                                           RequestContext(self.request, context))

    def send_messages(self):
        if hasattr(self, "success_message"):
            messages.success(self.request,
                             self.success_message % self.object)

    def write_historic(self):
        if hasattr(self, "historic_action"):
            self.request.user.register_historic(self.object,
                                                self.historic_action)
    def final_reponse(self):
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        # Permissao de salvar
        if hasattr(self, "save_permission"):
            if not self.request.user.has_perm(self.save_permission):
                return render(self.request, 'access_denied.html', locals())

        self.object = form.save()

        # Regstra o objeto no historico
        self.write_historic()

        # Grava mensagem de successo
        self.send_messages()
        
        return self.final_reponse()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(HFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(HFormView, self).post(request, *args, **kwargs)

class HttpRedirectException(Exception):
    """
    utilizada para redirecionar no meio de um processo interrompido
    """
    pass

class ManagementForm(forms.Form):
    current_step = forms.CharField(widget=forms.HiddenInput)

class WizardView(TemplateView):
    object = None
    form_instance = None #instancia de um formulario salvo
    object = None
    form_instance = None #instancia de um formulario salvo
    allow_redirect = False
    allow_cancel = False
    # nome, campo, formulario
    steps = ()
    step_count = 0

    def get_template_names(self):
        raise NotImplementedError

    def get_object(self, autocreate=True):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        """
        Metodo get
        usado para exibir a primeira pagina
        por isso é mais simples
        """

        action = self.request.GET.get('action', None)

        self.current_step = 0 #Iniciando o wizard
        self.step_count = self.num_steps()
        
        continue_step = self.request.GET.get('continue', None)

        if continue_step and continue_step.isdigit():
            step = self.steps[int(continue_step)]

            if getattr(step, 'allow_continue', False):
                self.current_step = int(continue_step)


        # Edição de um campo
        edit_step = self.request.GET.get('edit', None)
        if edit_step and edit_step.isdigit():
            step = self.steps[int(edit_step)]

            if getattr(step, 'allow_edit', False):
                self.current_step = int(edit_step)
        
        self.object = self.get_object() #busca por um objeto não salvo

        #Valida o edit
        if edit_step:
            if not self.get_form_instance():
                self.current_step = 0

        if action == 'cancel' and self.allow_cancel:
            self.object.delete()
            self.object = self.get_object()

        return self.render()

    def post(self, *args, **kwargs):
        """
        Metodo post
        utilizado para o recebimento dos dados e apresentar a proxima etapa
        """

        # busca pelo form de gerencia de steps
        management_form = ManagementForm(self.request.POST, prefix='wiz')
        if not management_form.is_valid():
            raise ValidationError(
                'ManagementForm data is missing or has been tampered.')

        self.current_step = int(management_form.cleaned_data['current_step'])
        self.step_count = self.num_steps()

        # so permite a criação do objeto se estiver preenchido a primeira etapa
        if self.current_step == 0:
            self.object = self.get_object()
        else:
            self.object = self.get_object(autocreate=False)
        
        if not self.object:
            raise HttpResponseForbidden

        # busca o formulário pelos dados fornecidos
        form = self.get_form(data=self.request.POST)

        if form.is_valid():
            self.save_step(form)
            
            if hasattr(form, 'get_success_url') and self.allow_redirect:
                return HttpResponseRedirect(form.get_success_url(self.object))

            if self.current_step >= len(self.steps) -1:
                return self.render_done(form, **kwargs)

            else:
                 #salva dados
                self.current_step += 1
                return self.render()

        return self.render(form)

    def render_done(self, form, **kwargs):
        raise NotImplementedError

    def save_step(self, form):
        """
        salva uma etapa no documento não salvo
        """
        data = form.save(commit=False)
        attr = self.get_form_attr()     

        if attr:
            setattr(self.object, attr, data)

        self.object.save() #validate=False)

    def render(self, form=None, **kwargs):
        """
        Returns a ``HttpResponse`` containing a all needed context data.
        """
        form = form or self.get_form()
        context = self.get_context_data(form, **kwargs)
        return self.render_to_response(context)

    def get_form(self, data=None, step=None):
        """
        retorna o formulário autal
        """
        if not step:
            step = self.current_step
        
        self.form_instance = self.get_form_instance()
        form = self.steps[step](data=data,
                                instance=self.form_instance)

        if hasattr(form, 'filter_object'):
            form.filter_object(self.object)

        if hasattr(form, 'filter_request'):
            form.filter_request(self.request)

        return form

    def get_form_label(self):
        """
        Retorna o label do formulário atual
        """
        return self.steps[self.current_step].label

    def get_form_attr(self):
        """
        Retorna o attributo do formulário atual
        """
        obj = self.steps[self.current_step]

        if hasattr(obj, 'attr'):
            return obj.attr
    
    def get_form_instance(self):
        """
        retorna a instancia do forumúlario atual
        """
        attr = self.get_form_attr()

        if attr:
            return getattr(self.object, attr)
    
    def num_steps(self):
        return len(self.steps)
    
    def get_context_data(self, form, *args, **kwargs):
        context = super(WizardView, self).get_context_data(*args, **kwargs)

        context['object'] = self.object
        context['form'] = form
        context['form_label'] = self.get_form_label()
        context['steps'] = self.steps
        context['form_instance'] = self.form_instance
        
        initial = {'current_step': self.current_step}

        context['management_form'] =  ManagementForm(prefix='wiz', initial=initial)

        return context
