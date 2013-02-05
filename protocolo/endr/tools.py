# -*- coding: utf-8 -*-

__all__ = ('SocialBairroImporter',)

import urllib

from bson import ObjectId
from django.utils import simplejson as json
from lethusbox.django.models import SettingValue

from .models import *

class SocialBairroImporter(object):
    def __init__(self):
        self.url = SettingValue.get('SOCIAL_URL')

    def _import_distrito_node(self, node):
        """
        Importa um nó json de um distrito
        """
        obj = Distrito.objects(social_pk=ObjectId(node['_pk'])).first()

        if not obj:
            obj = Distrito(social_pk=ObjectId(node['_pk']))

        obj.nome = node['nome']
        obj.mun = node['municipio']
        obj.save()

    def _import_bairro_node(self, node):
        """
        Importa um nó json de um bairro
        """
        obj = Bairro.objects(social_pk=ObjectId(node['_pk'])).first()

        if not obj:
            obj = Bairro(social_pk=ObjectId(node['_pk']))

        obj.nome = node['nome']
        obj.mun = node['municipio']
        
        if node.has_key('distrito'):
            obj.distrito = Distrito.objects(
                social_pk=ObjectId(node['distrito'])).first()
        else:
            obj.distrito = None

        obj.save()

    def sync(self):
        try:
            uo = urllib.urlopen('%ssaude-webservice/?cmd=get_distritos' % self.url)
            data = json.loads(uo.read())
        except IOError:
            return False
        else:
            for node in data:
                self._import_distrito_node(node)
        
        try:
            uo = urllib.urlopen('%ssaude-webservice/?cmd=get_bairros' % self.url)
            data = json.loads(uo.read())
        except IOError:
            return False
        else:
            for node in data:
                self._import_bairro_node(node)

        return True
