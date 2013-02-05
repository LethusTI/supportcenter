# -*- coding: utf-8 -*-

__all__ = ('Distrito', 'Bairro', 'Endereco')

from mongoengine import *
from lethusbox.municipios.models import MunicipioBrasil

class Distrito(Document):
    codigo = SequenceField(primary_key=True)

    social_pk = ObjectIdField(
        required=False,
        verbose_name="Chave primária no Lethus social")

    nome = StringField(
        verbose_name="Nome",
        required=True,
        max_length=150)

    mun = IntField(
        verbose_name="Código IBGE do Município",
        required=True)

    meta = {'allow_inheritance': False,
            'collection': 'endr.distrito'}

class Bairro(Document):
    codigo = SequenceField(primary_key=True)
    nome = StringField(
        verbose_name="Nome",
        required=True,
        max_length=150)

    social_pk = ObjectIdField(
        required=False,
        verbose_name="Chave primária no Lethus social")

    distrito = ReferenceField(
        Distrito,
        verbose_name="Distrito",
        required=False)

    mun = IntField(
        verbose_name="Código IBGE do Município",
        required=True)

    meta = {'allow_inheritance': False,
            'collection': 'endr.bairro'}

    @property
    def mun_obj(self):
        return MunicipioBrasil.objects.with_id(self.mun)
    
    def get_full_mun_display(self):
        obj = self.mun_obj

        if obj:
            return u"%s - %s" % (obj.nome, obj.uf_sigla)

    def __unicode__(self):
        return self.nome

class EnderecoMixIn(object):
    log = StringField(
        verbose_name="Logradouro",
        max_length=200,
        required=True)

    comp = StringField(
        verbose_name="Complemento",
        max_length=150,
        required=False)

    num = StringField(
        verbose_name=u"Número",
        max_length=100,
        required=False)

    cep = StringField(
        verbose_name="CEP",
        required=False,
        max_length=16)

    bairro = ReferenceField(
        Bairro,
        verbose_name="Bairro",
        required=False)

    distrito = ReferenceField(
        Distrito,
        verbose_name="Distrito",
        required=False)

    mun = IntField(
        verbose_name="Código IBGE do Município",
        required=True)

    @property
    def mun_obj(self):
        return MunicipioBrasil.objects.with_id(self.mun)

    def clean_sync_format(self, data):
        if self.mun:
            mun = self.mun_obj
        else:
            mun = None

        if mun:
            data['uf'] = mun.uf_sigla

        return data
        
class Endereco(EnderecoMixIn, EmbeddedDocument):
    meta = {'allow_inheritance': False}
