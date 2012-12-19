# -*- coding: utf-8 -*-

__all__ = ('SetorForm',)

from mongotools.forms import MongoForm
from django import forms

from models import Setor

class SetorForm(MongoForm):
    chefia = forms.ChoiceField(label="Chefia", required=False)
    
    class Meta:
        document = Setor
    
    def clean_chefia(self):
        pk = self.cleaned_data['chefia']
        if pk:
            obj = Setor.objects(pk=pk).first()
            return obj
        else: 
            return

    def __init__(self, *args,  **kwargs):
        super(SetorForm, self).__init__(*args,**kwargs)
       
        filter_args = {}
        if self.instance.pk:
            filter_args['pk__ne'] = self.instance.pk

        self.fields['chefia'].choices = [('','----------')]+[
            (str(s.pk), s.nome) for s in Setor.objects(**filter_args)]
