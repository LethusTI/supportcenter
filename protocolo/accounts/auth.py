# -*- coding: utf-8 -*-

from django.contrib.auth.models import AnonymousUser
from models import User
from django.core.validators import email_re
import datetime

REDIRECT_FIELD_NAME = 'next'

class MongoEngineBackend(object):
    """
    Backend de autenticação
    utilizada para validar e retornar a instancia de um usuário
    """
    
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        """
        Retorna o usuário atraves do username ou email e password.
        se não encontrar retorna None.
        """
        # verifica se e um email
        if email_re.match(username):
            try:
                user = User.objects(email=username).first()
            except User.DoesNotExist:
                return None

        # caso nao autentica no modo padrao
        else:
            try:
                user = User.objects(username=username).first()
            except User.DoesNotExist:
                return None

        if user:
            if password and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        return User.objects.with_id(user_id)

def get_user(userid):
    """
    Retorna o usuário atravez do sua identificação
    """
    if not userid:
        return AnonymousUser()
    return MongoEngineBackend().get_user(userid) or AnonymousUser()
