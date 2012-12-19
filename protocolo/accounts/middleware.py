# -*- coding: utf-8 -*-
import re

from django.shortcuts import render
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from lethusbox.django.responses import HttpRedirectException
from social.apps.accounts.models import UnidadeProfile, AdminProfile

# Otimizações nas regex compilando elas antes
AdminRegex = re.compile(r'/admin/.*')


class PermissionMiddleware(object):
    """
    Middleware usado para definir se o usuario que esta acesando e um administrador,
    ou usuário
    """

    def process_denied(self, request, reason=None):
        return render(request, 'access_denied.html', locals())

    def process_exception(self, request, exception):
        """
        Existe uma exeception nossa utilizada para
        Redirecionar para uma página no meio do processo
        ela é tratada aqui
        """

        if isinstance(exception, HttpRedirectException):
            return HttpResponseRedirect(exception.args[0])

        #if isinstance(exception, NotImplementedError):
        #    return render(request, 'not_implemented.html', locals())

    def process_request(self, request):
        if (AdminRegex.match(request.path) and
             (not isinstance(request.user, AdminProfile))):

            if not request.user.is_active:
                return self.process_denied(request,
                            "Seu usuário está inativo no sistema")

            return redirect_to_login(request.path)

        
