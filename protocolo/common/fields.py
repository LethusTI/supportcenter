# -*- coding: utf-8 -*

import datetime

from django.forms.fields import ChoiceField, MultipleChoiceField
from django.forms.fields import DateField
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field, DecimalField, DateField as OldDateField
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput, RadioSelect
from constants import HUMAN_DATE_FORMAT, MONGO_OBJECTID_SIZE
import re
from decimal import Decimal

MONEY_RE = re.compile(r'(R\$)? (?P<value>.*)')
MONGO_RE = re.compile(r'^[[0-9]|[a-f]]{24}$')

class MongoObjectIdChoiceField(ChoiceField):
    def valid_value(self, value):
        return bool(MONGO_RE.match(value))

class ObjectIdMultipleChoiceField(MultipleChoiceField):
    def valid_value(self, value):
        return bool(MONGO_RE.match(value))

class MongoDateField(DateField):
    def to_python(self, *args, **kwargs):
        val = super(MongoDateField, self).to_python(*args, **kwargs)
        
        if isinstance(val, datetime.date):
            return datetime.datetime(val.year, val.month, val.day)

        return val

from django.forms.widgets import TextInput

class NumberInput(TextInput):
    input_type = 'number'


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


class BRCPFCNPJField(Field):
    """
This field validate a CPF number or a CPF string. A CPF number is
compounded by XXX.XXX.XXX-VD. The two last digits are check digits. If it fails it tries to validate a CNPJ number or a CNPJ string. A CNPJ is compounded by XX.XXX.XXX/XXXX-XX.

More information:
http://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas
"""
    default_error_messages = {
        'invalid': _("CPF ou CNPJ Invalido."),
        'digits_only': _("E aceito apenas numeros."),
        'max_digits': _("Esse campo requer 11 digitos para CPF ou 14 digitos para CNPJ."),
    }

    def validate_CPF(self, value):
        """
Value can be either a string in the format XXX.XXX.XXX-XX or an
11-digit number.
"""
        if value in EMPTY_VALUES:
            return u''
        if not value.isdigit():
            value = re.sub("[-\.]", "", value)
        orig_value = value[:]
        try:
            int(value)
        except ValueError:
            raise ValidationError(self.error_messages['digits_only'])
        if len(value) != 11:
            raise ValidationError(self.error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise ValidationError(self.error_messages['invalid'])

        return orig_value

    def validate_CNPJ(self, value):
        ## Try to Validate CNPJ
        """
Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
group of 14 characters.
"""
        if value in EMPTY_VALUES:
            return u''
        if not value.isdigit():
            value = re.sub("[-/\.]", "", value)
        orig_value = value[:]
        try:
            int(value)
        except ValueError:
            raise ValidationError(self.error_messages['digits_only'])
        if len(value) != 14:
            raise ValidationError(self.error_messages['max_digits'])
        orig_dv = value[-2:]

        new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(5, 1, -1) + range(9, 1, -1))])
        new_1dv = DV_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(6, 1, -1) + range(9, 1, -1))])
        new_2dv = DV_maker(new_2dv % 11)
        value = value[:-1] + str(new_2dv)
        if value[-2:] != orig_dv:
            raise ValidationError(self.error_messages['invalid'])

        return orig_value
    

    def clean(self, value):

        value = super(BRCPFCNPJField, self).clean(value)
        try:
            orig_value = self.validate_CPF(value)
        except ValidationError:
            orig_value = self.validate_CNPJ(value)

        return orig_value


class MyEmailInput(TextInput):
    def __init__(self, *args, **kwargs):
        super(MyEmailInput, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'email'

class MyCepInput(TextInput):
    def __init__(self, *args, **kwargs):
        super(MyCepInput, self).__init__(*args, **kwargs)
        self.attrs.update({
            'maxlength': '9',
            'class':'cep',
        })

class MyPhoneInput(TextInput):
    def __init__(self, *args, **kwargs):
        super(MyPhoneInput, self).__init__(*args, **kwargs)
        self.attrs.update({
            'maxlength': '14',
            'class':'tel',
        })

class DateField(OldDateField):
    input_formats = [HUMAN_DATE_FORMAT]

class MoneyInput(DecimalField):
    def __init__(self, *args, **kwargs):
        super(MoneyInput, self).__init__(*args, **kwargs)
        self.widget.attrs.update({'class':'money'})
        
    def clean(self, value):
        if not value and not self.required:
            return None
        
        o = value
        
        if not o and not value.isdigit():
            if not self.required:
                return None

            raise ValidationError(u"Formatação Inválida")

        if o:
            value = o.replace('.', '').replace(',', '.')

        return super(MoneyInput, self).clean(value)

class MyDecimal(DecimalField):        
    def clean(self, value):
        if not value and not self.required:
            return None
        
        o = value

        if o:
            value = o.replace('.', '').replace(',', '.')

        return super(MyDecimal, self).clean(value)