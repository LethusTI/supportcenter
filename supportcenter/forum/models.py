# -*- coding: utf-8 -*-

__all__ = ('Forum', 'Reply')

import datetime
import django
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from mongoengine import *
from mongoengine.queryset import QuerySet, Q
from mongoengine import signals

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
        required=True,
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
            return _("Anonymous")

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

    def get_absolute_url(self):
        return '/forum/update/%d/' % self.id


        

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