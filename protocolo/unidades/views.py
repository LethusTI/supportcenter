# -*- coding: utf-8 -*-

__all__ = ('ListUnidadeView', 'AddUnidadeView', 'UpdateUnidadeView')

from lethusbox.django.responses import HybridListView
from mongotools.views import CreateView, UpdateView

from models import *
from forms import *

class ListUnidadeView(HybridListView):
    document = Unidade
    paginate_by = 20
    allow_empty = True
    json_object_list_fields = ['id', 'nome']
    sort_fields = ['id', 'nome']
    filter_fields = ['nome']
    template_name = "unidade/list.html"


class UnidadeViewMixIn(object):
    document = Unidade
    form_class = UnidadeForm
    success_url = '/admin/unidades/'

class AddUnidadeView(UnidadeViewMixIn, CreateView):
    success_message = "A Unidade \"%s\" foi criada com sucesso"
    historic_action = "unidade.add"

class UpdateUnidadeView(UnidadeViewMixIn, UpdateView):
    success_message = "A Unidade \"%s\" foi alterada com sucesso"
    historic_action = "unidade.update"
