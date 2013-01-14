# -*- coding: utf-8 -*

__all__ = ('MongoObjectIdChoiceField',
           'ObjectIdMultipleChoiceField',
           'MongoDateField', 'NumberInput',
           'BRCPFCNPJField', 'BRPhoneNumberField',
           'MoneyInput')

import re

from django.forms.fields import (
    ChoiceField, MultipleChoiceField, DateField,
    Field, DecimalField)

from django.utils.translation import ugettext_lazy as _

from .widgets import *

MONEY_RE = re.compile(r'(R\$)? (?P<value>.*)')
MONGO_RE = re.compile(r'^[[0-9]|[a-f]]{24}$')
phone_digits_re = re.compile(r'^(\d{2})[-\.]?(\d{4})[-\.]?(\d{4}\d?)$')

class MongoObjectIdFieldMixIn(object):
    """
    MixIn para permitir que um campo aceite valores de chaves primarias do MongoDB
    """
    def valid_value(self, value):
        return bool(MONGO_RE.match(value))

class MongoObjectIdChoiceField(MongoObjectIdFieldMixIn, ChoiceField):
    """
    ChoiceField que aceita apenas chaves primárias do mongodb
    """
    pass


class ObjectIdMultipleChoiceField(MongoObjectIdFieldMixIn, MultipleChoiceField):
    """
    MultipleChoiceField que aceita apenas chaves primárias do mongodb
    """
    pass

class MongoDateField(DateField):
    """
    Em mongoDB todo campo do tipo data aceita apenas valores datetime.
    este campo permite que aceite também objetos datetime.date
    """
    def to_python(self, *args, **kwargs):
        val = super(MongoDateField, self).to_python(*args, **kwargs)
        
        if isinstance(val, datetime.date):
            return datetime.datetime(val.year, val.month, val.day)

        return val

class BRCPFCNPJField(Field):
    """
    Campo para formulário que aceita tanto CPF quando CNPJ.
    """
    default_error_messages = {
        'invalid': u"CPF ou CNPJ inválido.",
        'digits_only': u"É aceito apenas números.",
        'max_digits': u"Esse campo requer 11 dígitos para CPF ou 14 digitos para CNPJ.",
    }

    @classmethod
    def dv_maker(self, v):
        """
        calcula o digito verificador
        """
        if v >= 2:
            return 11 - v

        return 0

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
        new_1dv = self.dv_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
        new_2dv = self.dv_maker(new_2dv % 11)
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
        new_1dv = self.dv_maker(new_1dv % 11)
        value = value[:-2] + str(new_1dv) + value[-1]
        new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(6, 1, -1) + range(9, 1, -1))])
        new_2dv = self.dv_maker(new_2dv % 11)
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

class MoneyInput(DecimalField):
    """
    Campo usado para guardar dinheiro em Decimal
    """
    widget = MoneyWidget

    def clean(self, value):
        if not value and not self.required:
            return None
        
        o = MONEY_RE.match(value)
        
        if not o and not value.isdigit():
            if not self.required:
                return None

            raise ValidationError(u"Formatação Inválida")

        if o:
            value = o.group('value').replace('.', '').replace(',', '.')

        return super(MoneyInput, self).clean(value)

class BRPhoneNumberField(Field):
    """
    Campo para telefones brasileiros, já acertado para aceitar telefones com 9 digitos.
    """
    widget = BRPhoneNumberInput
    default_error_messages = {
        'invalid': _('Phone numbers must be in XX-XXXX-XXXX format.'),
    }

    def clean(self, value):
        super(BRPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\(|\)|\s+)', '', smart_unicode(value))
        m = phone_digits_re.search(value)
        if m:
            return u'%s-%s-%s' % (m.group(1), m.group(2), m.group(3))
        raise ValidationError(self.error_messages['invalid'])
