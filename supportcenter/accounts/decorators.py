# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from models import User

def permission_required(function, perm, admin=True):
    """
    Usado para pedir permissoes
    """
    def call(request, *args, **kwargs):
        if not admin and isinstance(request.user, AdminProfile):
            reason = u"Acesso apenas para não-administradores"
            return render(request, 'access_denied.html', locals())

        if isinstance(perm, basestring) and request.user.has_perm(perm):
            return function(request, *args, **kwargs)

        elif isinstance(perm, (tuple, list)):
            for p in perm:
                if request.user.has_perm(p):
                    return function(request, *args, **kwargs)

        return render(request, 'access_denied.html', locals())

    return call

def cargo_login_required(function, cargo, unid_tp=None):
    """
    Usado para permitir acesso por cargo
    """
    def call(request, *args, **kwargs):
        if (isinstance(request.user, UnidadeProfile) and
            request.user.cargo == cargo):

            if not(unid_tp and request.user.unidade.tipo != unid_tp):
                return function(request, *args, **kwargs)

        return render(request, 'access_denied.html', 
                      {'reason': u"Acesso não autorizado para seu cargo ou unidade"})

    return call

def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("/auth/login/")
        
        return function(request, *args, **kwargs)
    return _inner
