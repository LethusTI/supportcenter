# -*- coding: utf-8 -*-

__all__ = ('PERMISSIONS_HEADERS', 'PERMISSIONS',
           'HISTORIC_GENERIC_ACTION_LABELS',
           'HISTORIC_EXCLUDE_COMMON_MODULES',
           'HISTORIC_CUSTOM_ACTIONS',
           'HISTORIC_MODULES_NAMES',
           'PERMISSIONS_NAMES',
           'USER_GROUP_FLAGS')

from django.utils.datastructures import SortedDict
def generate_perms(name, perms=None):
    """
    Gera as 4 permissões de um CRUD
    http://http://pt.wikipedia.org/wiki/CRUD
    :param name: nome da permissão
    """
    if not perms:
        perms = PERMISSIONS_NAMES

    return ['{0}.{1}'.format(name, x) for x in perms]

PERMISSIONS_NAMES = ('view', 'add', 'update', 'delete')
PERMISSIONS_HEADERS = ('Visualizar', 'Adicionar', 'Editar', 'Apagar')

PERMISSIONS = SortedDict((
        (u"Profissionais", generate_perms('profissionais', ('view', 'add', 'update'))),
))

PERMISSIONS.keyOrder.sort()

HISTORIC_GENERIC_ACTION_LABELS = {
        'add':  u"Criação",
        'update': u"Alteração",
        'delete': u"Remoção",
        'view': "Ver detalhes",
}

# módulos que não contem todas as 3 ações acima
HISTORIC_EXCLUDE_COMMON_MODULES = (
    'auth', 'atend', 'agenda', 'recurso'
)

HISTORIC_CUSTOM_ACTIONS = {
    'auth': {
        'login': "Login",
        'logout': "Logout",
        'changepassword': u"Alteração de senha",
        'changeprofile': u"Alteração dos dados pessoais"
        },
    'user': {
        'changepassword': u"Alteração de senha",
        },
    'superuser': {
        'changepassword': u"Alteração de senha",
        },
}

HISTORIC_MODULES_NAMES = SortedDict((
        ('superuser', "Administradores"),
        ('user', u"Usuários"),
        ('usergroup', u"Grupo de usuários"),
        ('unidade', "Unidades"),
        ('auth', u"Autenticação"),
        ('bairro', u"Bairros")
))

USER_GROUP_FLAGS = (
    ('a', "Utilizar todas as permissões do grupo"),
    ('c', "Personalizar")
)
