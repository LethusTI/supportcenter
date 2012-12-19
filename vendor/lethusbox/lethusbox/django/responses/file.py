# -*- coding: utf-8 -*-

import os
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

class TempFileResponse(HttpResponse):
    """
    usado para enviar Arquivos temporários
    para o cliente
    """
    def __init__(self, input_file, filename, *args, **kwargs):
        wrapper = FileWrapper(input_file)

        super(TempFileResponse, self).__init__(wrapper, *args, **kwargs)
        self['Content-Length'] = input_file.tell()
        input_file.seek(0)
        self['Content-Disposition'] = 'attachment; filename=%s' % filename
