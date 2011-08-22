# -*- coding: utf-8 -*-

from social.tools.responses.json import JSONResponse
from django.contrib import messages
from django.views.generic.base import View

class MassAction(View):
    """
    Classe abstrata para representar as ações em comum em um modelo
    """

    document = None
    http_method_names = ['post']

    def get_ids(self):
        return self.request.POST.getlist('ids[]')

    def get_object(self, id):
        """
        Valida e retorna objeto via id
        """
        return self.document.objects.get(id=id)

    def set_inactive(self):
        """
        Seta o conjunto de ids para inativos
        """
        if hasattr(self, 'perm_inactive'):
            if not self.request.user.has_perm(self.perm_inactive):
                return JSONResponse({'ok': False, 'error': 'Permissão Negada'})

        count = 0
        first_obj = None
        
        for id in self.get_ids():
            try:
                obj = self.get_object(id)
            except self.document.DoesNotExist:
                continue

            obj.is_active = False
            obj.save()
            count += 1

            if count == 1:      # guarda o primeiro obj
                first_obj = obj

            if hasattr(self, "action_inactive"):
                self.request.user.register_historic(obj,
                                                    self.action_inactive)

        if count == 1:
            messages.success(self.request, self.msg_inactive % first_obj)
        elif count > 1:
            messages.success(self.request, self.msg_inactive_plural % count)

        return JSONResponse({'ok': True})

    def set_active(self):
        """
        Seta o conjuto de ids para ativos
        """
        if hasattr(self, 'perm_active'):
            if not self.request.user.has_perm(self.perm_active):
                return JSONResponse({'ok': False, 'error': 'Permissão Negada'})

        count = 0
        first_obj = None

        for id in self.get_ids():
            try:
                obj = self.get_object(id)
            except self.document.DoesNotExist:
                continue

            obj.is_active = True
            obj.save()
            count += 1

            if count == 1:      # guarda o primeiro obj
                first_obj = obj

            if hasattr(self, "action_active"):
                self.request.user.register_historic(obj,
                                                    self.action_active)

        if count == 1:
            messages.success(self.request, self.msg_active % first_obj)
        elif count > 1:
            messages.success(self.request, self.msg_active_plural % count)

        return JSONResponse({'ok': True})

    def mass_delete(self):
        """
        Apaga em massa
        """
        if hasattr(self, 'perm_delete'):
            if not self.request.user.has_perm(self.perm_delete):
                return JSONResponse({'ok': False, 'error': 'Permissão Negada'})

        count = 0
        first_obj = None
        first_msg_delete = None

        for id in self.get_ids():
            try:
                obj = self.get_object(id)
            except self.document.DoesNotExist:
                continue

            count += 1

            if hasattr(self, "action_delete"):
                self.request.user.register_historic(obj,
                                                    self.action_delete)

            if count == 1:      # guarda o primeiro obj
                first_obj = obj
                first_msg_delete = self.msg_delete % first_obj

            obj.delete()

        if count == 1 and first_msg_delete:
            messages.success(self.request, first_msg_delete)
        elif count > 1:
            messages.success(self.request, self.msg_delete_plural % count)

        return JSONResponse({'ok': True})

    def post(self, request, *args, **kwargs):
        self.request = request
        cmd = self.request.POST.get('cmd', '')
        
        if cmd == 'mass_delete':
            return self.mass_delete()
        elif cmd == 'set_active':
            return self.set_active()
        elif cmd == 'set_inactive':
            return self.set_inactive()

        raise Http404
