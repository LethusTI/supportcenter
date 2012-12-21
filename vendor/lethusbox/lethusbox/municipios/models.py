
# -*- coding: utf-8 -*-

__all__ = ('UFBrasil', 'MunicipioBrasil')

from mongoengine import *
from constants import UF_CHOICES


class UFBrasil(Document):
    """
    Representa um estado do brasil,
    utilizado apenas para consulta.
    
    atributos:

    * codigo: código ibge do estado
    * sigla: sigla do estado
    * nome: nome do estado
    * regiao: região do estado
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
    Representa um município do brasil.
    é utilizado apenas para consulta

    atributos:

    * codigo: código ibge do município
    * nome: nome completo do município
    * uf_sigla: sigla do estado do município
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
        """
        Retorna o município no formato json 
        pronto para ser enviado via ajax
        """
        return {'codigo': self.codigo,
                'nome': self.nome,
                'uf': self.uf_sigla}

if not UFBrasil.objects.first() or not MunicipioBrasil.objects.first():
    from .utils import Loader
    print "Carregando municipios e estados brasileiros"
    loader = Loader()
    loader.load()
