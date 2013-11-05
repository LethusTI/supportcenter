# -*- coding: utf-8 -*-

__all__ = ('AddForumForm', 'AddReplyForm')

from mongotools.forms import MongoForm
from django import forms
from lethusbox.django.fields import BRPhoneNumberField

from .models import *

def AddForumForm(user, *args, **kwargs):
    """
    Fabricamos o formulário em tempo de execução:
    http://pt.wikipedia.org/wiki/Factory_Method

    Usamos assim para que o formulário seja criado ajustado para o
    tipo de usuário que está acessando
    """
    exclude_fields = ['user', 'date']

    if not user.is_anonymous():
        exclude_fields.extend(['name', 'email', 'phone'])
    
    class _AddForumForm(MongoForm):
        if user.is_anonymous():
            phone = BRPhoneNumberField(
                label = Forum.phone.verbose_name,
                required = True,
                error_messages={'invalid' :u"Número de telefone inválido!"})

        title = forms.CharField(
            label=Forum.title.verbose_name,
            required=Forum.title.required,
            widget=forms.TextInput(attrs={'class': 'span5'}))

        comment = forms.CharField(
            label=Forum.comment.verbose_name,
            required=Forum.comment.required,
            widget=forms.Textarea(attrs={'class': 'input-xxlarge'}))
    
        def __init__(self, user, *args, **kwargs):
            super(_AddForumForm, self).__init__(*args, **kwargs)
            self.user = user

        def save(self, commit=True):
            obj = super(_AddForumForm, self).save(commit=False)
        
            if not obj.user and not self.user.is_anonymous():
                obj.user = self.user
                obj.name = self.user.get_full_name()[0:64]
                obj.email = self.user.email
    
            if commit:
                obj.save()
    
            return obj

        class Meta:
            document = Forum
            exclude = tuple(exclude_fields)

    return _AddForumForm(user, *args, **kwargs)

def AddReplyForm(user, *args, **kwargs):
    """
    Fabricamos o formulário em tempo de execução:
    http://pt.wikipedia.org/wiki/Factory_Method

    Usamos assim para que o formulário seja criado ajustado para o
    tipo de usuário que está acessando
    """
    exclude_fields = ['user', 'date', 'forum']

    if not user.is_anonymous():
        exclude_fields.extend(['name', 'email', 'phone'])
        
    class _AddReplyForm(MongoForm):
        if user.is_anonymous():
            phone = BRPhoneNumberField(
                label = Reply.phone.verbose_name,
                required = Reply.phone.required,
                error_messages={'invalid' :u"Número de telefone inválido!"})
 
        reply = forms.CharField(
            label=Reply.reply.verbose_name,
            required=Reply.reply.required,
            widget=forms.Textarea(attrs={'class': 'input-xxlarge'}))
    
        def __init__(self, user, forum, *args, **kwargs):
            super(_AddReplyForm, self).__init__(*args, **kwargs)
            self.user = user
            self.forum = forum

        def save(self, commit=True):
            obj = super(_AddReplyForm, self).save(commit=False)
            if not obj.user and not self.user.is_anonymous():
                obj.user = self.user
                obj.name = self.user.get_full_name()[0:64]
                obj.email = self.user.email
            
            obj.forum = self.forum
            
            if commit:
                obj.save()

            return obj

        class Meta:
            document = Reply
            exclude = exclude_fields

    return _AddReplyForm(user, *args, **kwargs)
