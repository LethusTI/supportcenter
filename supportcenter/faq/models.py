# -*- coding: utf-8 -*-

__all__ = ('Category', 'CategoryProxy', 'Question')

#from knowledge import settings
import datetime
import django
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from mongoengine import *
from mongoengine.queryset import QuerySet, Q
from mongoengine import signals

#from knowledge.managers import QuestionManager, ResponseManager

class CategoryProxy(object):
    """
    Proxy de acesso a categorias e filtrar por categoria
    """
    def __init__(self, queryset, user):
        self.queryset = queryset
        self.user = user

    def __iter__(self):
        for category in self.queryset:
            category._access_user = self.user
            yield category
        
class Category(Document):
    added = DateTimeField(default=datetime.datetime.now)
    lastchanged = DateTimeField(default=datetime.datetime.now)

    title = StringField(max_length=255, required=True, verbose_name=_('Title'))
    slug = StringField(required=True)

    position = IntField(
        verbose_name=_("Position"),
        required=False)
    
    def clean(self):
        self.lastchanged = datetime.datetime.now()

    def __unicode__(self):
        return self.title

    def get_faq_queryset(self):
        filter_kwargs = {'categories': self}
        
        if hasattr(self, '_access_user'):
            if self._access_user.is_anonymous():
                filter_kwargs['locked'] = False

        return Question.objects(**filter_kwargs)
    
    def faq_count(self):
        return self.get_faq_queryset().count()

    def last_by_date(self):
        return self.get_faq_queryset().order_by('added')[0:5]
    
    meta = {
        'ordering': ['title'],
    }

class KnowledgeBase(Document):
    added = DateTimeField(default=datetime.datetime.now)
    lastchanged = DateTimeField(default=datetime.datetime.now)
    user = ReferenceField(
        'User',
        verbose_name=u"Criado por usuário",
        required=False)
    
    get_email = lambda s: s.user.email
    
    def clean(self):
        self.lastchanged = datetime.datetime.now()

    def get_name(self):
        """
        Get local name, then self.user's first/last, and finally
        their username if all else fails.
        """
        name = self.user and (
             u'{0} {1}'.format(self.user.first_name, self.user.last_name or '').strip()\
             or self.user.username
        )
        if name:
            return name.strip()
        
    meta = {
        'abstract': True
    }

class QuestionQuerySet(QuerySet):
    def can_view(self, user):
        if user.is_anonymous():
            return self.filter(locked=False)
        
        return self

class Question(KnowledgeBase):
    id = SequenceField(
        verbose_name="Identification",
        primary_key=True)
    
    title = StringField(
        max_length=255,
        verbose_name=_('Question'),
        required=True,
        help_text=_('Enter your question or suggestion.'))
    
    body = StringField(
        required=True,
        verbose_name=_('Description'),
        help_text=_('Please offer details. Markdown enabled.'))

    locked = BooleanField(
        default=False,
        verbose_name=_("View access only for superusers"))

    categories = ListField(
        ReferenceField(Category),
        verbose_name=_("Categories"))


    meta = {
        'ordering': ['-added'],
        'queryset_class': QuestionQuerySet
    }

    def __unicode__(self):
        return self.title

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return '/faq/questions/%d/' % self.id

    def get_categories_display(self):
        if self.categories:
            return ', '.join([str(c) for c in self.categories])
        
        return ''
