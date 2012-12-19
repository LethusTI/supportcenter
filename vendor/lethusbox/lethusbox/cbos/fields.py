# -*- coding: utf-8 -*-

from django.forms.fields import ChoiceField

class OcupacaoChoiceField(ChoiceField):
    def valid_value(self, value):
        return True
