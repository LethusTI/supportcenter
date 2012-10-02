# -*- coding: utf-8 -*-

__all__ = ('Ocupacao',)

from mongoengine import *

class Ocupacao(Document):
    """
    Representa uma ocupação
    """
    codigo = IntField(
        verbose_name=u"Código",
        primary_key=True)

    nome = StringField(
        verbose_name="Nome",
        required=True)

    meta = {'allow_inheritance': False,
            'ordering': ['nome'],
            'indexes': [
                {'fields': ['nome', 'codigo']}
            ],
            'collection': 'ocupacao'}

if not Ocupacao.objects.first():
    from .utils import Loader
    print "Carregando ocupações"
    loader = Loader()
    loader.load()
