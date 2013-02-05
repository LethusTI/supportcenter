# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.dates import MONTHS
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.http import Http404

from mongoengine.django.shortcuts import get_document_or_404
from lethusbox.django.responses import HybridListView, HFormView
from mongotools.views import (
    CreateView, UpdateView)

from protocolo.common.output import json_response

from forms import (
    AccountForm, SuperUserForm, AddSuperUserForm,
    UnidadeProfileForm, AddUnidadeProfileForm,
    HistoricFilterForm, AdminPasswordChangeForm,
    UserGroupForm)

from models import (
    User, UnidadeProfile, Historic, UserGroup)
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
    success_message = u"O administrador \"%s\" foi criado com sucesso"

class UpdateSuperUserView(SuperUserOnlyEditableMixIn,
                          SuperUserViewMixIn, UpdateView):
    historic_action = "superuser.update"
    success_message = u"O administrador \"%s\" foi alterado com sucesso"

    def get_context_data(self, *args, **kwargs):
        ctx = super(UpdateSuperUserView, self).get_context_data(*args, **kwargs)
        ctx['form2'] = AdminPasswordChangeForm(self.request.user)

        return ctx

class SetPasswordSuperUserView(SuperUserOnlyEditableMixIn,
                               SuperUserViewMixIn, HFormView):
    historic_action = "superuser.changepassword"
    success_message = u"A Senha do administrador \"%s\" foi alterada com sucesso"

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

class UnidadeProfileViewMixIn(object):
    document = UnidadeProfile
    form_class = UnidadeProfileForm
    template_name = "user/form.html"
    success_url = "/admin/users/"
    get_services = ('get_group_perms',)

    def get(self, *args, **kwargs):
        cmd = self.request.GET.get('cmd')

        if cmd and cmd in self.get_services:
            return getattr(self, "_%s" % cmd)()

        return super(UnidadeProfileViewMixIn, self).get(*args, **kwargs)

    @json_response
    def _get_group_perms(self):
        group = get_document_or_404(
            UserGroup,
            pk=self.request.GET.get('group_id'))

        return group.permissions

class ListUnidadeProfileView(UnidadeProfileViewMixIn, HybridListView):
    paginate_by = 20
    allow_empty = True
    json_object_list_fields = ['id', 'username', 'get_full_name', 'email', 'unidade', 'is_active']
    sort_fields = ['id', 'username', 'first_name', 'email', 'unidade', 'is_active']
    filter_fields = ['username', 'first_name', 'last_name', 'email']
    template_name = "user/list.html"

class AddUnidadeProfileView(UnidadeProfileViewMixIn, CreateView):
    form_class = AddUnidadeProfileForm
    historic_action = "user.add"
    success_message = "O Usuário \"%s\" foi criado com sucesso"

class UpdateUnidadeProfileView(UnidadeProfileViewMixIn, UpdateView):
    historic_action = "user.update"
    success_message = "O Usuário \"%s\" foi alterado com sucesso"

    def get_context_data(self, *args, **kwargs):
        ctx = super(UpdateUnidadeProfileView, self).get_context_data(*args, **kwargs)
        ctx['form2'] = AdminPasswordChangeForm(self.request.user)
        ctx['password_tab'] = False

        return ctx

class SetPasswordUnidadeProfileView(UnidadeProfileViewMixIn, HFormView):
    historic_action = "user.changepassword"
    success_message = "A Senha do usuário \"%s\" foi alterada com sucesso"
    def get_form(self, form_class):
        """
        Hack para direcionar para o alterador de senha
        """
        return self.form_class(instance=self.get_object())

    def get_object(self):
        return get_document_or_404(
            self.document, pk=self.kwargs.get('pk'))

    def get_context_data(self, *args, **kwargs):
        context = super(SetPasswordUnidadeProfileView, self).get_context_data(*args, **kwargs)

        obj = self.get_object()

        context['object'] = obj
        context['password_tab'] = True
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
        return super(SetPasswordUnidadeProfileView, self).form_valid(form)

class CoreHistoricView(HybridListView):
    """
    Classe Base de Histórico
    ela lista os logs de um usuário
    e pode usar para saida em pdf, csv, json e html
    o get_object tem que ser validado na classe filha
    """
    model = Historic
    date_field = "dtime"
    filter_form = HistoricFilterForm
    paginate_by = 20
    allow_empty = True

    template_name = "history/history_view.html"
    csv_template_name = "history/history_view.csv"
    csv_filename = "historico.csv"

    pdf_template_name = "history/history_view.pdf.html"
    pdf_filename = "historico.pdf"

    json_object_list_fields = ['id', 'get_module_label',
                               'get_action_label', 'get_absolute_url',
                               'object', 'dtime']
    sort_fields = ['id', 'action', 'action', None, 'object', 'dtime']
    filter_fields = []

    def get_filtered_queryset(self, data, queryset):
        """
        Filtra a queryset segundo os dados do FilterForm
        data = cleaned_data do form
        queryset = uma queryset raiz que será filtrada

        retorna nova queryset com os filtros aplicados
        """

       
        if data['from_date'] and data['to_date']: #data inicial e data final
            queryset = queryset.filter(
                dtime__gte=datetime.datetime.combine(data['from_date'],
                                                     datetime.time.min),
                dtime__lte=datetime.datetime.combine(data['to_date'],
                                                     datetime.time.max))

            # com apenas data inicial ele filtra apenas o dia selecionado
        elif data['from_date'] and not data['to_date']:
            queryset = queryset.filter(
                dtime__gte=datetime.datetime.combine(data['from_date'],
                                                     datetime.time.min),
                dtime__lte=datetime.datetime.combine(data['from_date'],
                                                     datetime.time.max))

        # Filtro por Módulo
        module = data['module']
        action = data['action']

        if module:
            if not module in HISTORIC_MODULES_NAMES:
                raise Http404

            if action:
                queryset = queryset.filter(action=action)
            else:
                queryset = queryset.filter(action__startswith='%s.' % module)

        return queryset

    def get_queryset(self):
        filter = self.filter_form(self.request.GET,
                                  filter_module = self.filter_module,
                                  filter_action = self.filter_action)

        queryset = self.build_main_queryset()
        
        if filter.is_valid():
            return self.get_filtered_queryset(filter.cleaned_data, queryset)

        return queryset

    def get_extra_context(self):
        c = {'object': self.get_object(),}

        if hasattr(self, "filter_form"):
            c["filter_form"] = self.filter_form(self.request.GET,
                                                filter_module = self.filter_module,
                                                filter_action = self.filter_action)

        return c

    def filter_module(self):
        """
        metodo para listar todos os modulos de filtros disponiveis
        """
        return HISTORIC_MODULES_NAMES.items()

    def filter_action(self):
        """
        metodo para listar todas ações de modulos para filtros disponiveis
        """
        for key in HISTORIC_MODULES_NAMES.iterkeys():
            if key in HISTORIC_CUSTOM_ACTIONS:
                for act, label in HISTORIC_CUSTOM_ACTIONS[key].iteritems():
                    yield ('%s.%s' % (key, act), label)

            if key in HISTORIC_EXCLUDE_COMMON_MODULES:
                continue

            for act, label in HISTORIC_GENERIC_ACTION_LABELS.iteritems():
                yield ('%s.%s' % (key, act), label)

    def get_object(self):
        raise NotImplemented

    def build_main_queryset(self):
        """
        Monta a query principal que irá ser filtrada posteriormente
        """
        # Por padrao vem filtrando por usuário
        return self.model.objects.filter(user=self.get_object())

    @json_response
    def _get_action_list(self, module):
        data = [('', u"Todas Ações")]

        if not module in HISTORIC_EXCLUDE_COMMON_MODULES:
            for act, label in HISTORIC_GENERIC_ACTION_LABELS.iteritems():
                data.append(("%s.%s" % (module, act), label))

        if module in HISTORIC_CUSTOM_ACTIONS:
            for act, label in HISTORIC_CUSTOM_ACTIONS[module].iteritems():
                data.append(("%s.%s" % (module, act), label))

        return data

    def get(self, *args, **kwargs):
        cmd = self.request.GET.get('cmd', None)

        if cmd == 'get_action_list':
            module = self.request.GET.get('module', None)
            if module:
                return self._get_action_list(module)

        return super(CoreHistoricView, self).get(*args, **kwargs)

class HistoricSuperUserView(CoreHistoricView):
    def get_object(self):
        return get_document_or_404(
            User, pk=self.kwargs.get('pk', None),
            is_superuser=True)

class HistoricUnidadeProfileView(CoreHistoricView):
    def get_object(self):
        return get_document_or_404(
            UnidadeProfile, pk=self.kwargs.get('pk', None))

class GeneralHistoricView(CoreHistoricView):
    """
    usado para exibição dos logs gerais do sistema
    """
    template_name = "history/general_view.html"
    csv_template_name = "history/general_view.csv"
    csv_filename = "historico.csv"

    pdf_template_name = "history/general_view.pdf.html"
    pdf_filename = "historico.pdf"

    json_object_list_fields = ['id', 'get_user', 'get_module_label', 
                               'get_action_label', 'get_absolute_url',
                               'object', 'dtime']
    sort_fields = ['id', 'user', 'action', 'action', None, 'object', 'dtime']
    filter_fields = []

    def get_object(self):
        return

    def build_main_queryset(self):
        return self.model.objects

class ListUserGroupView(HybridListView):
    document = UserGroup
    paginate_by = 20
    allow_empty = True
    json_object_list_fields = ['id', 'nome']
    filter_fields = ['nome']
    template_name = "user/group_list.html"

class UserGroupMixInView(object):
    document = UserGroup
    form_class = UserGroupForm
    template_name = "user/group_form.html"
    success_url = '/admin/users/groups/'

class AddUserGroupView(UserGroupMixInView, CreateView):
    historic_action = "usergroup.add"
    success_message = "O grupo de usuários \"%s\" foi criado com sucesso"

class UpdateUserGroupView(UserGroupMixInView, UpdateView):
    historic_action = "usergroup.update"
    success_message = "O grupo de usuários \"%s\" foi atualizado com sucesso"
