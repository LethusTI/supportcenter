# -*- coding: utf-8 -*-

__all__ = ('AddSetorView', 'EditSetorView')

from lethusbox.django.responses import HybridListView
from mongotools.views import CreateView, UpdateView

from models import Setor
from forms import SetorForm 

class AddSetorView(CreateView):
    document = Setor
    form_class = SetorForm
    success_url = "/admin/setores/"
    historic_action = "setores.add"

class EditSetorView(UpdateView):
    document = Setor
    form_class = SetorForm
    success_url = "/admin/setores/"
    historic_action = "setores.update"

class ListSetorView(HybridListView):
    document = Setor
    paginate_by = 20
    allow_empty = True 
    json_object_list_fields = ['id', 'sigla', 'nome', 'chefia.sigla', 'chefia.nome']
    sorted_fields = ['id', 'sigla', 'nome', 'chefia.sigla', 'chefia.nome']
    filter_fields = ['sigla', 'nome']
    template_name = "setor/list.html"
    

