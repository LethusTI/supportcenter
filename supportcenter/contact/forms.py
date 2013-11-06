# -*- coding: utf-8 -*-

__all__ = ('AddContactForm',)

from django import forms
from lethusbox.django.fields import BRPhoneNumberField
from django.utils.translation import ugettext_lazy as _

class AddContactForm(forms.Form):
    nome = forms.CharField(
        label=_('Name'),
        required=True,
        max_length=64, 
        widget=forms.TextInput(attrs={'class': 'span5'}),
        help_text=_('Enter your first and last name.'))

    phone = BRPhoneNumberField(
        label = _('Phone'),
        required = True,
        error_messages={'invalid' :u"Número de telefone inválido!"})

    email = forms.EmailField(
        label=_("E-mail"), 
        max_length=75,
        help_text=_('Enter a valid email address.'))

    subject = forms.CharField(
        label=_('Subject'),
        required=True,
        widget=forms.TextInput(attrs={'class': 'span5'}))

    message = forms.CharField(
        label=_('Message'),
        required=True,
        widget=forms.Textarea(attrs={'class': 'input-xxlarge'}))


    def __init__(self, *args, **kwargs):
        super(AddContactForm, self).__init__(*args, **kwargs)
            