# -*- coding: utf-8 -*-

__all__ = ('Category', 'Question')

#from knowledge import settings
import datetime
import django
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from mongoengine import *
from mongoengine.queryset import QuerySet, Q
from mongoengine import signals

#from knowledge.managers import QuestionManager, ResponseManager
from .signals import knowledge_post_save

class Category(Document):
    added = DateTimeField(default=datetime.datetime.now)
    lastchanged = DateTimeField(default=datetime.datetime.now)

    title = StringField(max_length=255, required=True, verbose_name=_('Title'))
    slug = StringField(required=True)

    def clean(self):
        self.lastchanged = datetime.datetime.now()
    
    def __unicode__(self):
        return self.title

    def faq_count(self):
        return Question.objects(categories=self).count()

    def last_by_date(self):
        return Question.objects(categories=self).order_by('added')[0:5]
    
    meta = {
        'ordering': ['title']
    }

class KnowledgeBase(Document):
    added = DateTimeField(default=datetime.datetime.now)
    lastchanged = DateTimeField(default=datetime.datetime.now)
    
    user = ReferenceField(
        'User',
        verbose_name=u"Criado por usuário",
        required=False)

    name = StringField(
        max_length=64, required=False,
        verbose_name=_('Name'),
        help_text=_('Enter your first and last name.'))
    
    email = EmailField(
        required=False,
        verbose_name=_('Email'),
        help_text=_('Enter a valid email address.'))
    
    get_email = lambda s: s.email or (s.user and s.user.email)

    
    
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
        else:
            return _("Anonymous")
        
    meta = {
        'abstract': True
    }

class QuestionQuerySet(QuerySet):
    def can_view(self, user):
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

    locked = BooleanField(default=False)

    categories = ListField(
        ReferenceField(Category))


    meta = {
        'ordering': ['-added'],
        'queryset_class': QuestionQuerySet
    }

    def __unicode__(self):
        return self.title

    def inherit(self):
        pass

    def internal(self):
        pass

    def lock(self, save=True):
        self.locked = not self.locked
        if save:
            self.save()
    lock.alters_data = True

    ###################
    #### RESPONSES ####
    ###################

    def get_responses(self, user=None):
        return []
        #user = user or self._requesting_user
        if user:
            return [r for r in self.responses.all().select_related('user') if r.can_view(user)]
        else:
            return self.responses.all().select_related('user')

    def answered(self):
        """
        Returns a boolean indictating whether there any questions.
        """
        return bool(self.get_responses())

    def accepted(self):
        """
        Returns a boolean indictating whether there is a accepted answer
        or not.
        """
        return any([r.accepted for r in self.get_responses()])

    def clear_accepted(self):
        self.get_responses().update(accepted=False)
    clear_accepted.alters_data = True

    def accept(self, response=None):
        """
        Given a response, make that the one and only accepted answer.
        Similar to StackOverflow.
        """
        self.clear_accepted()

        if response and response.question == self:
            response.accepted = True
            response.save()
            return True
        else:
            return False
    accept.alters_data = True

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return '/faq/questions/%d/' % self.id

    def get_categories_display(self):
        if self.categories:
            return ', '.join([str(c) for c in self.categories])
        return ''
    

signals.post_save.connect(knowledge_post_save, sender=Question)
