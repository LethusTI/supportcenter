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

        if created:
            print "Atualizando municipio %s do estado %s" % (
                mun.nome, mun.uf_sigla)
        else:
            print "Criando municipio %s do estado %s" % (
                mun.nome, mun.uf_sigla)

    def _load_uf(self, node):
        uf, created = UFBrasil.objects.get_or_create(
            pk=node['pk'], auto_save=False)

        uf.sigla = node['fields']['uf']
        uf.regiao = node['fields']['regiao']
        uf.nome = node['fields']['nome']
        uf.save()

        if created:
            print "Atualizando o estado %s" % uf.nome
        else:
            print "Criando o estado %s" % uf.nome

    def load(self):
        """
        Dá carga no banco de dados
        """
        for node in json.loads(self.data):
            if node['model'] == 'municipios.municipio':
                self._load_municipio(node)
            elif node['model'] == 'municipios.uf':
                self._load_uf(node)
