# -*- coding: utf-8 -*-

__all__ = ('Loader',)

import os
from bz2 import decompress
from django.utils import simplejson as json
from models import *

class Loader(object):
    """
    Responsável por pré carregar os municipios e estados brasileiros
    """
    def __init__(self):
        compressed = open(
            os.path.join(os.path.dirname(__file__),
                         'database',
                         'municipios.json.bz2'))

        self.data = decompress(compressed.read())

    def _load_municipio(self, node):
        mun, created = MunicipioBrasil.objects.get_or_create(
            pk=node['pk'], auto_save=False)
        mun.uf_sigla = node['fields']['uf_sigla']
        mun.nome = node['fields']['nome']
        mun.save()

    def _load_uf(self, node):
        uf, created = UFBrasil.objects.get_or_create(
            pk=node['pk'], auto_save=False)

        uf.sigla = node['fields']['uf']
        uf.regiao = node['fields']['regiao']
        uf.nome = node['fields']['nome']
        uf.save()

    def load(self):
        """
        Dá carga no banco de dados
        """
        for node in json.loads(self.data):
            if node['model'] == 'municipios.municipio':
                self._load_municipio(node)
            elif node['model'] == 'municipios.uf':
                self._load_uf(node)
