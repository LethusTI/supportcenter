# -*- coding: utf-8 -*-

__all__ = ('Unidade',)

from mongoengine import *

class Organizacao(Document):
    nome = StringField(verbose_name="Nome resumido",
                       max_length=50, required=True)
    telefone = StringField(verbose_name="Telefone",
                           db_field="tel",
                           max_length=18)
    meta = {'collection': 'org',
            'allow_inheritance': True}

    def __unicode__(self):
        return self.nome

class Unidade(Organizacao):
    pass
    
