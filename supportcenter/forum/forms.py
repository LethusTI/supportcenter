# -*- coding: utf-8 -*-

__all__ = ('AddForumForm', 'AddReplyForm')

from mongotools.forms import MongoForm
from django import forms
from lethusbox.django.fields import BRPhoneNumberField


from .models import *

class AddForumForm(MongoForm):
    phone = BRPhoneNumberField(
        label = Forum.phone.verbose_name,
        required = Forum.phone.required,
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
        super(AddForumForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        obj = super(AddForumForm, self).save(commit=False)
        
        if not obj.user and not self.user.is_anonymous():
            obj.user = self.user
    
        if commit:
            obj.save()
    
        return obj

    class Meta:
        document = Forum
        exclude = ('user', 'date')


class AddReplyForm(MongoForm):
    phone = BRPhoneNumberField(
        label = Reply.phone.verbose_name,
        required = Reply.phone.required,
        error_messages={'invalid' :u"Número de telefone inválido!"})

 
    reply = forms.CharField(
        label=Reply.reply.verbose_name,
        required=Reply.reply.required,
        widget=forms.Textarea(attrs={'class': 'input-xxlarge'}))
    
    forum = forms.ChoiceField(
        label=Reply.forum.verbose_name,
        required=Reply.forum.required,
        )
    def __init__(self, user, forum, *args, **kwargs):
        super(AddReplyForm, self).__init__(*args, **kwargs)
        self.user = user
        self.forum = forum

    def save(self, commit=True):
        obj = super(AddReplyForm, self).save(commit=False)
        if not obj.user and not self.user.is_anonymous():
            obj.user = self.user
        
        obj.forum = self.forum
        if commit:
            obj.save()

        return obj

    class Meta:
        document = Reply
        exclude = ('user', 'date', 'forum')