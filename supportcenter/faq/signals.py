def send_alerts(target_dict, response=None, question=None, **kwargs):
    """
    This can be overridden via KNOWLEDGE_ALERTS_FUNCTION_PATH.
    """
    from supportcenter.accounts.models import User
    from django.template.loader import render_to_string
    from django.core.mail import EmailMultiAlternatives
    from supportcenter.settings import DEPLOY_URL
    
    for email, name in target_dict.items():
        if isinstance(name, User):
            name = u'{0} {1}'.format(name.first_name, name.last_name)
        else:
            name = name[0]

        context = {
            'name': name,
            'email': email,
            'response': response,
            'question': question,
            'site': {
                'domain': DEPLOY_URL,
                'name': "Lethus support center"
            }
        }

        subject = render_to_string(
            'faq/emails/subject.txt', context)

        message = render_to_string(
            'faq/emails/message.txt', context)

        message_html = render_to_string(
            'faq/emails/message.html', context)

        subject = u' '.join(line.strip() for line in subject.splitlines()).strip()
        msg = EmailMultiAlternatives(subject, message, to=[email])
        msg.attach_alternative(message_html, 'text/html')
        msg.send()

def knowledge_post_save(sender, document, created):
    """
    Gathers all the responses for the sender's parent question
    and shuttles them to the predefined module.
    """
    from .models import Question, Response
    from supportcenter.accounts.models import User

    if created:
        # pull together the out_dict:
        #    {'e@ma.il': ('first last', 'e@ma.il') or <User>}
        ## if isinstance(document, Response):
        ##     instances = list(instance.question.get_responses())
        ##     instances += [instance.question]

        ##     # dedupe people who want alerts thanks to dict keys...
        ##     out_dict = dict([[i.get_email(), i.get_user_or_pair()]
        ##                     for i in instances if i.alert])

        if isinstance(document, Question):
            staffers = User.objects.filter(is_superuser=True)
            out_dict = dict([[user.email, user] for user in staffers])

        # remove the creator...
        if document.get_email() in out_dict.keys():
            del out_dict[document.get_email()]

        send_alerts(
            target_dict=out_dict,
            response=document if isinstance(document, Response) else None,
            question=document if isinstance(document, Question) else None
        )
