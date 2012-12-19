# -*- coding: utf-8 -*-

__all__ = ('Loader',)

import os
from bz2 import decompress
from django.utils import simplejson as json
from models import *

class Loader(object):
    """
    Responsável por pré carregar as ocupações
    """
    def __init__(self):
        compressed = open(
            os.path.join(os.path.dirname(__file__),
                         'database',
                         'cbos.json.bz2'))

        self.data = decompress(compressed.read())

    def _load_node(self, node):
        obj = Ocupacao(codigo=int(node[0]), nome=node[1])
        obj.save()
        
    def load(self):
        """
        Dá carga no banco de dados
        """
        for node in json.loads(self.data):
            self._load_node(node)
