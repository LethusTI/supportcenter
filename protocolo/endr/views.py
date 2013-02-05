# -*- coding: utf-8 -*-

__all__ = ('ListBairroView', 'AddBairroView',
           'UpdateBairroView', 'EndrServiceMixIn')

from django.shortcuts import redirect
from django.contrib import messages

from lethusbox.django.responses import HybridListView
from lethusbox.municipios.models import MunicipioBrasil
from lethusbox.django.decorators import json_response
from lethusbox.django.models import SettingValue

from mongotools.views import CreateView, UpdateView

from .models import *
from .tools import SocialBairroImporter
from .forms import *

class EndrServiceMixIn(object):
    get_services = ('get_municipios',
                    'get_distritos',
                    'get_bairros',
                    'get_distrito_bairros')

    @json_response
    def _get_municipios(self):
        objs = MunicipioBrasil.objects(
            uf_sigla = self.request.GET.get('uf', None)).order_by('nome')

        return [(o.codigo, o.nome) for o in objs]

    @json_response
    def _get_distritos(self):
        objs = Distrito.objects(
            mun = self.request.GET.get('mun_id', None)).order_by('nome')

        return [(o.codigo, o.nome) for o in objs]

    @json_response
    def _get_bairros(self):
        objs = Bairro.objects(
            mun = self.request.GET.get('mun_id', None),
            distrito=None).order_by('nome')

        return [(o.codigo, o.nome) for o in objs]

    @json_response
    def _get_distrito_bairros(self):
        objs = Bairro.objects(
            distrito=int(self.request.GET.get('dst_id')))

        return [(o.codigo, o.nome) for o in objs]

    def get(self, *args, **kwargs):
        cmd = self.request.GET.get('cmd', None)

        if cmd and cmd in self.get_services:
            return getattr(self, "_%s" % cmd)()

        return super(EndrServiceMixIn, self).get(*args, **kwargs)

class BairroViewMixIn(EndrServiceMixIn):
    document = Bairro
    form_class = BairroForm
    template_name = "bairro/form.html"
    success_url = "/admin/bairros/"

class ListBairroView(BairroViewMixIn, HybridListView):
    paginate_by = 20
    allow_empty = True
    json_object_list_fields = ['id', 'nome', 'distrito.nome', 'get_full_mun_display']
    sort_fields = ['id', 'nome', 'distrito', 'mun']
    filter_fields = ['nome']
    template_name = "bairro/list.html"
    get_services = BairroViewMixIn.get_services + ('import_from_social',)

    def _import_from_social(self):
        if SettingValue.get_bool('INTEGRATE_SOCIAL'):
            s = SocialBairroImporter()
            
            if s.sync():
                messages.success(self.request, "Importação dos bairros realizada com sucesso")
            else:
                messages.error(self.request, "Falha na importação dos bairros")

        return redirect(self.success_url)

    def get_context_data(self, *args, **kwargs):
        ctx = super(ListBairroView, self).get_context_data(*args, **kwargs)
        ctx['integrate_social'] = SettingValue.get_bool('INTEGRATE_SOCIAL')
        return ctx

class AddBairroView(BairroViewMixIn, CreateView):
    success_message = "O bairro \"%s\" foi criado com sucesso"
    historic_action = "bairro.add"

class UpdateBairroView(BairroViewMixIn, UpdateView):
    success_message = "O bairro \"%s\" foi alterado com sucesso"
    historic_action = "bairro.update"
