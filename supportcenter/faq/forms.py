# -*- coding: utf-8 -*-

__all__ = ('AddQuestionForm', 'AdminQuestionForm',
           'CategoryForm')

from mongotools.forms import MongoForm

from .utils import slugify
from .models import *

class AddQuestionForm(MongoForm):
    def __init__(self, user, *args, **kwargs):
        super(AddQuestionForm, self).__init__(*args, **kwargs)

        self.user = user

    def save(self, commit=True):
        obj = super(AddQuestionForm, self).save(commit=False)
        obj.user = self.user
        
        if commit:
            obj.save()
        
        return obj
    
    class Meta:
        document = Question
        fields = ('title', 'body')

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
