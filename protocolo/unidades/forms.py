# -*- coding: utf-8 -*-

__all__ = ('UnidadeForm',)

from mongotools.forms import MongoForm
from lethusbox.django.fields import BRPhoneNumberField

from models import *

class UnidadeForm(MongoForm):
    telefone = BRPhoneNumberField(
        label=Unidade.telefone.verbose_name,
        required=Unidade.telefone.required)

    class Meta:
        document = Unidade
