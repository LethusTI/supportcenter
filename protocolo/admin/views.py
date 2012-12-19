# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.core.servers.basehttp import FileWrapper

from forms import AdminSettingsForm

from protocolo.common.models import ImageConstant

class AdminSettingsView(FormView):
    form_class = AdminSettingsForm
    template_name = "admin/settings.html"
    success_url = "/"

    def form_valid(self, form, *args, **kwargs):
        form.save()
        messages.success(self.request,
                         "Configurações alteradas com sucesso, por favor reinicie o serviço de aplicação")
        return super(AdminSettingsView, self).form_valid(form, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        ctx = super(AdminSettingsView, self).get_context_data(*args, **kwargs)
        
        ctx['brasao_atual'] = ImageConstant.has('brasao')

        return ctx

def image_constant(request, key):
    mimetypes = {'jpg': 'image/jpeg',
                 'png': 'image/png'}
    f_name = key

    parts = key.split('.', 2)
    key = parts[0]
    
    if len(parts) > 1:
        mimetype = mimetypes.get(parts[1], parts[1])
    else:
        mimetype = 'image/jpeg'

    f = ImageConstant.get_cached(key)

    if f:
        o_file = open(f)

        resp = HttpResponse(
            FileWrapper(o_file), mimetype=mimetype)
    
    return resp




