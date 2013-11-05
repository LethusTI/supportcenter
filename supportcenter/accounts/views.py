# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.dates import MONTHS
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from mongoengine.django.shortcuts import get_document_or_404
from lethusbox.django.responses import HybridListView, HFormView
from mongotools.views import (
    CreateView, UpdateView)

from supportcenter.common.output import json_response

from forms import (
    AccountForm, SuperUserForm, AddSuperUserForm,
    AdminPasswordChangeForm,
    UserGroupForm, HistoricFilterForm)

from models import (
    User, Historic, UserGroup)
from constants import *
from lethusbox.django.responses import HybridListView

class AccountSettingView(UpdateView):
    template_name = "generic/user_setting.html"
    success_url = "/"
    form_class = AccountForm
    success_message = "Seus dados pessoais foram alterados com sucesso"
    historic_action = "auth.changeprofile"

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(AccountSettingView, self).get_context_data(*args, **kwargs)
        context["form2"] = PasswordChangeForm(self.request.user)

        return context

class AccountSetPasswordView(HFormView):
    """
    Editor de Senhas
    form = Form de Editar o Usuario
    form2 = Form de Alterar Senha
    """
    template_name = "generic/user_setting.html"
    historic_action = "auth.changepassword"
    success_url = "/"
    form_class = PasswordChangeForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(AccountSetPasswordView, self).get_context_data(*args, **kwargs)
        context['object'] = self.get_object()
        context['form'] = AccountForm(instance=self.get_object())
        context['form2'] = PasswordChangeForm(self.get_object(), **self.get_form_kwargs())
        
        return context

    def get_form(self, form_class):
        """
        Hack para direcionar para o alterador de senha
        """
        return AccountForm(instance=self.get_object())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form2 = PasswordChangeForm(self.object, request.POST)

        if form2.is_valid():
            return self.form_valid(form2)
        else:
            return self.form_invalid(form2)

    def form_valid(self, form):
        """
        Quando valido altera a senha
        """
        self.object = form.save()

        messages.success(self.request,
                         "Sua Senha foi alterada com sucesso")

        return super(AccountSetPasswordView, self).form_valid(form)

class SuperUserViewMixIn(object):
    document = User
    form_class = SuperUserForm
    template_name = "superuser/form.html"
    success_url = "/admin/superusers/"

    def get_queryset(self):
        return self.document.objects(is_superuser=True)

class SuperUserOnlyEditableMixIn(object):
    not_editable_template_name = "superuser/not_editable.html"

    def get(self, *args, **kwargs):
        obj = self.get_object()

        if not obj.editable:
            return render(self.request, self.not_editable_template_name)
        
        return super(SuperUserOnlyEditableMixIn, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        obj = self.get_object()

        if not obj.editable:
            return render(self.request, self.not_editable_template_name)

        return super(SuperUserOnlyEditableMixIn, self).post(*args, **kwargs)
        

class ListSuperUserView(SuperUserViewMixIn, HybridListView):
    paginate_by = 20
    allow_empty = True
    json_object_list_fields = ['id', 'username', 'get_full_name', 'email', 'is_active']
    sort_fields = ['id', 'username', 'first_name', 'email', 'is_active']
    filter_fields = ['username', 'first_name', 'last_name', 'email']
    template_name = "superuser/list.html"

class AddSuperUserView(SuperUserViewMixIn, CreateView):
    form_class = AddSuperUserForm
    historic_action = "superuser.add"
    success_message = _("The \"%s\" admin was added successfully")

class UpdateSuperUserView(SuperUserOnlyEditableMixIn,
                          SuperUserViewMixIn, UpdateView):
    historic_action = "superuser.update"
    success_message = _("The \"%s\" admin was changed successfully")

    def get_context_data(self, *args, **kwargs):
        ctx = super(UpdateSuperUserView, self).get_context_data(*args, **kwargs)
        ctx['form2'] = AdminPasswordChangeForm(self.request.user)

        return ctx

class SetPasswordSuperUserView(SuperUserOnlyEditableMixIn,
                               SuperUserViewMixIn, HFormView):
    historic_action = "superuser.changepassword"
    success_message = _("The \"%s\" admin password was changed successfully")

    def get_form(self, form_class):
        """
        Hack para direcionar para o alterador de senha
        """
        return self.form_class(instance=self.get_object())

    def get_object(self):
        return get_document_or_404(
            User, pk=self.kwargs.get('pk'), is_superuser=True)

    def get_context_data(self, *args, **kwargs):
        context = super(SetPasswordSuperUserView, self).get_context_data(*args, **kwargs)

        obj = self.get_object()

        context['object'] = obj
        context['form'] = self.form_class(instance=obj)
        context['form2'] = AdminPasswordChangeForm(obj, **self.get_form_kwargs())
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form2 = AdminPasswordChangeForm(self.object, request.POST)

        if form2.is_valid():
            return self.form_valid(form2)
        else:
            return self.form_invalid(form2)
    
    def form_valid(self, form):
        """
        Quando valido altera a senha
        """
        self.object = form.save()
        return super(SetPasswordSuperUserView, self).form_valid(form)
