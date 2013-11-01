# -*- coding: utf-8 -*-

__all__ = ('Category', 'Question')

import datetime
import django
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from mongoengine import *
from mongoengine.queryset import QuerySet, Q
from mongoengine import signals

class Forum(Document):
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
    	)
	comment = StringField(
		verbose_name=_('Comment'),
		required=False,
		)