# -*- coding: utf-8 -*-

__all__ = ('CaptchaTextInput', 'CaptchaField')

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse,  NoReverseMatch
from django.forms import ValidationError
from django.forms.fields import CharField, MultiValueField
from django.forms.widgets import TextInput, MultiWidget, HiddenInput
from django.utils.translation import ugettext_lazy as _

from .models import CaptchaStore

class CaptchaTextInput(MultiWidget):
    def __init__(self, attrs=None, **kwargs):
        widgets = (
            HiddenInput(attrs),
            TextInput(attrs),
        )
        
        super(CaptchaTextInput, self).__init__(widgets, attrs)
      
    def decompress(self, value):
        if value:
            return value.split(',')
            
        return [None, None]

    def format_output(self, rendered_widgets):
        return ' '.join([self.image_url,]+ rendered_widgets)
        
    def render(self, name, value, attrs=None):
        store = CaptchaStore.generate_new_item()
        value = [store.hashkey, u'']
        
        self.image_url = '<img src="%s" alt="captcha" class="captcha" />' % reverse(
            'captcha-image', kwargs={'key': store.hashkey})
        
        return super(CaptchaTextInput, self).render(name, value, attrs=attrs)
        
    def id_for_label(self, id_):
        return id_ + '_1'

class CaptchaField(MultiValueField):
    widget = CaptchaTextInput
    
    def __init__(self, label="Digite o código abaixo",
                 *args, **kwargs):

        fields = (
            CharField(show_hidden_initial=True),
            CharField(),
        )
        if 'error_messages' not in kwargs or 'invalid' not in kwargs.get('error_messages'):
            if 'error_messages' not in kwargs:
                kwargs['error_messages'] = dict()
            kwargs['error_messages'].update(dict(invalid=_('Invalid CAPTCHA')))

        super(CaptchaField, self).__init__(fields=fields, label=label, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return ','.join(data_list)
        return None

    def clean(self, value):
        super(CaptchaField, self).clean(value)
        response, value[1] = value[1], ''        
        response = response.upper()

        CaptchaStore.remove_expired()

        store = CaptchaStore.objects(
            response=response, hashkey=value[0],
            expiration__gt=CaptchaStore.get_safe_now()).first()

        if not store:
            raise ValidationError(u'Captcha inválido')

        store.delete()
        return value
