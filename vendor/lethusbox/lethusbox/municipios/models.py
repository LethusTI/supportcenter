# -*- coding: utf-8 -*-

__all__ = ('UFBrasil', 'MunicipioBrasil')

from mongoengine import *
from constants import UF_CHOICES


class UFBrasil(Document):
    """
    Representa todos os estados do brasil
    não é utilizado como domínio do sistema.
    é utilizado apenas para consulta.
    """

    codigo = IntField(
        verbose_name=u"Código IBGE",
        primary_key=True)

    sigla = StringField(
        max_length=2,
        choices=UF_CHOICES)
    
    nome = StringField(max_length=100,
                       verbose_name="Nome")

    regiao = StringField(max_length=100,
                         verbose_name=u"Região")
    
    meta = {'allow_inheritance': False,
            'ordering': ['nome'],
            'indexes': [
               {'fields': ['codigo']},
               {'fields': ['sigla']},
            ],
            'collection': 'brasil.uf'}

class MunicipioBrasil(Document):
    """
    Representa todos os municipios do brasil.
    não é utilizado como domínio do sistema.
    é utilizado apenas para consulta
    """

    codigo = IntField(
        verbose_name=u"Código IBGE",
        primary_key=True)
    nome = StringField(max_length=100,
                       verbose_name="Nome")
    uf_sigla = StringField(
        max_length=2,
        choices=UF_CHOICES)
    
    meta = {'allow_inheritance': False,
            'ordering': ['sigla'],
            'indexes': [
               {'fields': ['codigo']},
            ],
            'collection': 'brasil.municipio'}

    def json_format(self):
        return {'codigo': self.codigo,
                'nome': self.nome,
                'uf': self.uf_sigla}

if not UFBrasil.objects.first() or not MunicipioBrasil.objects.first():
    from .utils import Loader
    print "Carregando municipios e estados brasileiros"
    loader = Loader()
    loader.load()
