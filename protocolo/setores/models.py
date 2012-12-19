# -*- coding: utf-8 -*-

__all__ = ('Setor',)

from mongoengine import * 
from lethusbox.mongoengine.fields import UpperStringField

class Setor(Document):
    sigla = UpperStringField(max_length=10, required=True, unique=True, verbose_name="Sigla")
    nome = StringField(max_length=100, required=True, unique=True, verbose_name="Nome")
    chefia = ReferenceField('Setor', verbose_name="Chefia", required=False)

    meta = {'alow_inheritane': False}

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return "/setores/update/%s/" % str(self.pk)
