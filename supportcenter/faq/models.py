# -*- coding: utf-8 -*-

__all__ = ('Category', 'Question')

#from knowledge import settings
import datetime
import django
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from mongoengine import *
from mongoengine.queryset import QuerySet, Q

#from knowledge.managers import QuestionManager, ResponseManager
#from knowledge.signals import knowledge_post_save

STATUSES = (
    ('public', _('Public')),
    ('private', _('Private')),
    ('internal', _('Internal')),
)


STATUSES_EXTENDED = STATUSES + (
    ('inherit', _('Inherit')),
)


class Category(Document):
    added = DateTimeField(default=datetime.datetime.now)
    lastchanged = DateTimeField(default=datetime.datetime.now)

    title = StringField(max_length=255, required=True)
    slug = StringField(required=True)

    def clean(self):
        self.lastchanged = datetime.datetime.now()
    
    def __unicode__(self):
        return self.title

    meta = {
        'ordering': ['title']
    }

class KnowledgeBase(Document):
    added = DateTimeField(default=datetime.datetime.now)
    lastchanged = DateTimeField(default=datetime.datetime.now)
    
    user = ReferenceField(
        'User',
        verbose_name=u"Criado por usuário",
        required=True)
    
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
        return name.strip() or _("Anonymous")
        
    meta = {
        'abstract': True
    }
    
        
## class KnowledgeBase(Document):
##     """
##     The base class for Knowledge models.
##     """
##     is_question, is_response = False, False

##     added = models.DateTimeField(auto_now_add=True)
##     lastchanged = models.DateTimeField(auto_now=True)

##     user = models.ForeignKey('auth.User' if django.VERSION < (1, 5, 0) else django_settings.AUTH_USER_MODEL, blank=True,
##                              null=True, db_index=True)
##     alert = models.BooleanField(default=settings.ALERTS,
##         verbose_name=_('Alert'),
##         help_text=_('Check this if you want to be alerted when a new'
##                         ' response is added.'))

##     

##     class Meta:
##         abstract = True

##     def save(self, *args, **kwargs):
##         if not self.user and self.name and self.email \
##                 and not self.id:
##             # first time because no id
##             self.public(save=False)

##         if settings.AUTO_PUBLICIZE and not self.id:
##             self.public(save=False)

##         super(KnowledgeBase, self).save(*args, **kwargs)

##     #########################
##     #### GENERIC GETTERS ####
##     #########################



##     get_email = lambda s: s.email or (s.user and s.user.email)
##     get_pair = lambda s: (s.get_name(), s.get_email())
##     get_user_or_pair = lambda s: s.user or s.get_pair()

##     ########################
##     #### STATUS METHODS ####
##     ########################

##     def can_view(self, user):
##         """
##         Returns a boolean dictating if a User like instance can
##         view the current Model instance.
##         """

##         if self.status == 'inherit' and self.is_response:
##             return self.question.can_view(user)

##         if self.status == 'internal' and user.is_staff:
##             return True

##         if self.status == 'private':
##             if self.user == user or user.is_staff:
##                 return True
##             if self.is_response and self.question.user == user:
##                 return True

##         if self.status == 'public':
##             return True

##         return False

##     def switch(self, status, save=True):
##         self.status = status
##         if save:
##             self.save()
##     switch.alters_data = True

##     def public(self, save=True):
##         self.switch('public', save)
##     public.alters_data = True

##     def private(self, save=True):
##         self.switch('private', save)
##     private.alters_data = True

##     def inherit(self, save=True):
##         self.switch('inherit', save)
##     inherit.alters_data = True

##     def internal(self, save=True):
##         self.switch('internal', save)
##     internal.alters_data = True

class QuestionQuerySet(QuerySet):
    def can_view(self, user):
        if user.is_staff or user.is_superuser:
            return self

        if user.is_anonymous():
            return self.filter(status='public')

        return self.filter(
            Q(status='public') | Q(status='private', user=user)
        )

class Question(KnowledgeBase):
    title = StringField(
        max_length=255,
        verbose_name=_('Question'),
        required=True,
        help_text=_('Enter your question or suggestion.'))
    
    body = StringField(
        required=True,
        verbose_name=_('Description'),
        help_text=_('Please offer details. Markdown enabled.'))

    status = StringField(
        verbose_name=_('Status'),
        max_length=32, choices=STATUSES,
        default='private')

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

    def states(self):
        """
        Handy for checking for mod bar button state.
        """
        return [self.status, 'lock' if self.locked else None]

    @property
    def url(self):
        return self.get_absolute_url()


class Response(Document):
    is_response = True
    body = StringField(
        required=True,
        verbose_name=_('Response'),
        help_text=_('Please enter your response. Markdown enabled.'))
    
    status = StringField(
        verbose_name=_('Status'),
        max_length=32, choices=STATUSES_EXTENDED,
        default='inherit')
    
    accepted = BooleanField(default=False)

    meta = {
        'ordering': ['added']
    }

    def __unicode__(self):
        return self.body[0:100] + u'...'

    def states(self):
        """
        Handy for checking for mod bar button state.
        """
        return [self.status, 'accept' if self.accepted else None]

    def accept(self):
        self.question.accept(self)
    accept.alters_data = True


# cannot attach on abstract = True... derp
#models.signals.post_save.connect(knowledge_post_save, sender=Question)
#models.signals.post_save.connect(knowledge_post_save, sender=Response)
