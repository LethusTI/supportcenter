# -*- coding: utf-8 -*-

__all__ = ('forum_post_save', 'reply_post_save')

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from supportcenter.accounts.models import User
from supportcenter.settings import DEPLOY_URL

def forum_post_save(sender, document, created):
    if created:
        staffers = User.objects.filter(is_superuser=True)
        out_dict = dict([[user.email, user] for user in staffers])

        for user in staffers:
            context = {
                'name': user.get_full_name(),
                'email': user.email,
                'topic': document,
                'site': {
                    'domain': DEPLOY_URL,
                    'name': "Lethus support center"
                }
            }
            
            subject = render_to_string(
                'forum/emails/new_topic_subject.txt', context)

            message = render_to_string(
                'forum/emails/new_topic_message.txt', context)

            message_html = render_to_string(
                'forum/emails/new_topic_message.html', context)

            subject = u' '.join(line.strip() for line in subject.splitlines()).strip()
            msg = EmailMultiAlternatives(subject, message, to=[user.email])
            msg.attach_alternative(message_html, 'text/html')
            msg.send()

def reply_post_save(sender, document, created):
    if created:
        staffers = User.objects.filter(is_superuser=True)
        out_dict = dict([[user.email, user.get_full_name()] for user in staffers])

        for reply in document.forum.replies:
            out_dict[reply.email] = reply.name

        for email, name in out_dict.iteritems():
            context = {
                'name': name,
                'email': email,
                'reply': document,
                'site': {
                    'domain': DEPLOY_URL,
                    'name': "Lethus support center"
                }
            }
            
            subject = render_to_string(
                'forum/emails/new_reply_subject.txt', context)

            message = render_to_string(
                'forum/emails/new_reply_message.txt', context)

            message_html = render_to_string(
                'forum/emails/new_reply_message.html', context)

            subject = u' '.join(line.strip() for line in subject.splitlines()).strip()
            msg = EmailMultiAlternatives(subject, message, to=[email])
            msg.attach_alternative(message_html, 'text/html')
            msg.send()
