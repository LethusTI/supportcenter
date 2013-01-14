# -*- coding: utf-8 -*

__all__ = ('NumberInput', 'HTML5EmailInput', 'CepInput',
           'BRPhoneNumberInput', 'MoneyWidget')

from django.forms.widgets import TextInput

class NumberInput(TextInput):
    """
    Widget de entrada de número funciona em HTML5
    """
    input_type = 'number'

class HTML5EmailInput(TextInput):
    """
    Widget de entrada de email funciona em HTML5
    """
    def __init__(self, *args, **kwargs):
        super(HTML5EmailInput, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'email'

class CepInput(TextInput):
    def __init__(self, *args, **kwargs):
        super(CepInput, self).__init__(*args, **kwargs)
        self.attrs.update({
            'maxlength': '9',
            'class':'cep',
        })

class BRPhoneNumberInput(TextInput):
    """
    Widget de entrada de telefones brasileiros
    """
    def __init__(self, *args, **kwargs):
        super(BRPhoneNumberInput, self).__init__(*args, **kwargs)
        self.attrs.update({
            'maxlength': '15',
            'class':'tel',
        })

class MoneyWidget(TextInput):
    """
    Widget de entrada de dinheiro (reais).
    """
    def _format_value(self, value):
        if isinstance (value, basestring):
            return value

        return ("R$ %0.2f" % value).replace('.', ',')
