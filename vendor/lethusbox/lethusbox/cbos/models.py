# -*- coding: utf-8 -*-

__all__ = ('Ocupacao',)

from mongoengine import *
from mongoengine.queryset import QuerySet

class OcupacaoQuerySet(QuerySet):
    def categoria(self, codigo_inicial, codigo_final=None):
        """
        Filtro por categoria.
        """
        if not codigo_final:
            codigo_final = codigo_inicial

        codigo_inicial = int("%d000" % codigo_inicial)
        codigo_final = int("%d999" % codigo_final)

        self.filter(codigo__gte=codigo_inicial,
                    codigo__lte=codigo_final)

        return self

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
            'queryset_class': OcupacaoQuerySet,
            'ordering': ['nome'],
            'indexes': [
                {'fields': ['nome', 'codigo']}
            ],
            'collection': 'ocupacao'}

    def __unicode__(self):
        return self.nome

if not Ocupacao.objects.first():
    from .utils import Loader
    print "Carregando ocupações"
    loader = Loader()
    loader.load()
