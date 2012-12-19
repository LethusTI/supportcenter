# -*- coding: utf-8 -*-

__all__ = ('UnidadeForm',)

from mongotools.forms import MongoForm

from models import *

class UnidadeForm(MongoForm):
    class Meta:
        document = Unidade
