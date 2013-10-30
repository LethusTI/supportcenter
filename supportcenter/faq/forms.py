# -*- coding: utf-8 -*-

__all__ = ('AddQuestionForm', 'AdminQuestionForm',
           'CategoryForm')

from mongotools.forms import MongoForm

from .utils import slugify
from .models import *

def AddQuestionForm(user, *args, **kwargs):

    if user.is_anonymous():
        sfields = ['name', 'email', 'title', 'body']
    else:
        sfields = ['title', 'body']

    class _AddQuestionForm(MongoForm):
        def __init__(self, user, *args, **kwargs):
            super(_AddQuestionForm, self).__init__(*args, **kwargs)

            self.user = user

        def save(self, commit=True):
            obj = super(_AddQuestionForm, self).save(commit=False)
            if not obj.user and not self.user.is_anonymous():
                obj.user = self.user
        
            if commit:
                obj.save()
        
            return obj
    
        class Meta:
            document = Question
            fields = sfields

    return _AddQuestionForm(user, *args, **kwargs)

class AdminQuestionForm(MongoForm):
    def __init__(self, user, *args, **kwargs):
        super(AdminQuestionForm, self).__init__(*args, **kwargs)
        self.user = user
        
    def save(self, commit=True):
        obj = super(AdminQuestionForm, self).save(commit=False)

        if not obj.user:
            obj.user = self.user
        
        if commit:
            obj.save()
        
        return obj
    
    class Meta:
        document = Question
        exclude = ('user', 'added', 'lastchanged')

class CategoryForm(MongoForm):

    def save(self, commit=True):
        obj = super(CategoryForm, self).save(commit=False)

        if not obj.slug:
            obj.slug = slugify(obj.title)
        
        if commit:
            obj.save()
        
        return obj
    class Meta:
        document = Category
        fields = ('title',)
