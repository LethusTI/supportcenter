# -*- coding: utf-8 -*-

__all__ = ('PERMISSIONS_HEADERS', 'PERMISSIONS',
           'HISTORIC_GENERIC_ACTION_LABELS',
           'HISTORIC_EXCLUDE_COMMON_MODULES',
           'HISTORIC_CUSTOM_ACTIONS',
           'HISTORIC_MODULES_NAMES',
           'PERMISSIONS_NAMES')

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
        (u"Planos de saúde", generate_perms('plano_saude', ('view', 'add', 'update'))),
        (u"Pessoas", generate_perms('pessoas', ('view', 'add', 'update'))),
        (u"Vacinas", generate_perms('vacinas', ('view', 'add', 'update'))),
        (u"Campanhas", generate_perms('campanhas', ('view', 'add', 'update'))),
        (u"Fornecedores", generate_perms('fornecedores', ('view', 'add', 'update'))),
        (u"Lote de vacinas", generate_perms('lotevacinas', ('view', 'add', 'update'))),
        (u"Vacinação", generate_perms('vacinacao', ('view', 'add'))),
        (u"Evento adverso", generate_perms('eventoadverso', ('add',))),
        (u"Relatórios de vacinações", generate_perms('vacinarelatorio', ('view',))),
        (u"Medicamentos", generate_perms('medicamentos', ('view', 'add', 'udpate'))),
        (u"Fabricantes", generate_perms('fabricantes', ('view', 'add', 'udpate'))),
        
        (u"Entrada de medicamentos", generate_perms('medicamentos_entradaestoque', ('view',))),
        (u"Dispensacao de medicamentos", generate_perms('medicamentos_dispensacao', ('view',))),
        (u"Devolução de medicamentos", generate_perms('medicamentos_devolucao', ('view',))),
        (u"Ajuste de estoque de medicamentos", generate_perms('medicamentos_aje', ('view',))),
        (u"Ajuste de lote de medicamentos", generate_perms('medicamentos_ajl', ('view',))),
        (u"Relatório de medicamentos", generate_perms('farmaciarelatorio', ('view',))),
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
    'eventoadverso': {
        'register': "Registro"
        },
    'vacinacao': {
        'cardeneta': "Geração/Impressão de cardeneta"
        }
}

HISTORIC_MODULES_NAMES = SortedDict((
        ('superuser', "Administradores"),
        ('user', u"Usuários"),
        ('unidade', "Unidades"),
        ('auth', u"Autenticação"),
        ('bairro', u"Bairros"),
        ('profissional', u"Profissional"),
        ('plano_saude', u"Plano de saúde"),
        ('pessoa', u"Pessoa"),
        ('faixa_etaria', u"Faixa etária"),
        ('vacina', u"Vacina"),
        ('campanha', u"Campanha"),
        ('fornecedor', u"Fornecedor"),
        ('lotevacina', u"Lote de vacina"),
        ('vacinacao', u"Vacinação"),
        ('eventoadverso', u"Evento adverso"),
        ('medicamento', u"Medicamento"),
        ('fabricante', u"Fabricante")
))
