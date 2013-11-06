# -*- coding: utf-8 -*-

__all__ = ('Forum', 'Reply')

import datetime
import django
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from mongoengine import *
from mongoengine.queryset import QuerySet, Q
from mongoengine import signals

from .signals import *

class ForumBase(Document):
    id = SequenceField(
        primary_key=True)

    user = ReferenceField(
        'User',
        verbose_name=_('Create by user'),
        required=False)

    name = StringField(
        max_length=64, 
        required=True,
        verbose_name=_('Name'),
        help_text=_('Enter your first and last name.'))

    email = EmailField(
        required=True,
        verbose_name=_('Email'),
        help_text=_('Enter a valid email address.'))

    phone = StringField(
        verbose_name=_('Phone'),
        # falso apenas para o banco de dados
        # caso o admin responda nao alocar o phone
        required=False,
        help_text=_('Enter a valid phone number.'))

    date = DateTimeField(
        required=True,
        verbose_name =_('creation date'),
        default=datetime.datetime.now
        )
    
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
            return self.name

    meta = {
        'abstract': True,
        'indexes': [
            {'fields': ['email']},
            {'fields': ['user']},
            ]
    }

class Forum(ForumBase):
    title = StringField(
        verbose_name=_('Post Title'),
        required=True)

    comment = StringField(
        verbose_name=_('Comment'),
        required=True)

    meta = {
        'indexes': [
            {'fields': ['title']}
        ]
    }
    @property
    def replies(self):
        queryset = Reply.objects(forum=self).order_by('date')
        return queryset

    def get_absolute_url(self):
        return '/forum/%d/' % self.id

    def get_delete_url(self):
        return '/forum/delete/%d/' % self.id

    @property
    def url(self):
        return self.get_absolute_url()

class Reply(ForumBase):
    reply = StringField(
        verbose_name=_('Reply'),
        required=True)

    forum = ReferenceField(
        Forum,
        dbref=False,
        )

    meta = {
        'indexes': [
            {'fields': ['forum']}
        ]
    }

    def get_absolute_url(self):
        return '/forum/%d/#reply-%d' % (
            self.forum.id, self.id)

    @property
    def url(self):
        return self.get_absolute_url()

    def get_delete_reply_url(self):
        return '/forum/reply/%d/delete/' % self.id
        
signals.post_save.connect(forum_post_save, sender=Forum)
signals.post_save.connect(reply_post_save, sender=Reply)
