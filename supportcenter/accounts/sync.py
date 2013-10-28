# -*- coding: utf-8 -*-

from social.apps.sync.base import SyncModule

class TabletUsers(SyncModule):
    """
    Serviço de sincronicação para o tablet
    fornece lista de usuário e senha.
    """
    def fetch(self, tablet, options):
        from social.apps.accounts.models import UnidadeProfile

        data = []
        for u in UnidadeProfile.objects(is_active=True):
            data.append(u.sync_format())

        return data

    class Meta:
        name = "tablet_users"
