# -*- coding: utf-8 -*

__all__ = ('json_response',)

import ho.pisa as pisa

from django.http import HttpResponse
from django.template.loader import render_to_string

from lethusbox.django.responses.json import JSONResponse


try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def json_response(f):
    """
    Decorator para fornecer uma função que retorna uma resposta em JSON
    """
    def func(*args, **kwargs):
        return JSONResponse(f(*args, **kwargs))

    func.__name__ = f.__name__
    func.__doc__ = f.__doc__

    return func

class PDFView(object):
    def __init__(self, object, template):
        self.object = object
        self.template = template

    def render(self, name=None):

        if isinstance(self.object, dict):
            html = render_to_string(
                self.template, self.object)
        else:
            html = render_to_string(
                self.template, {'object': self.object})

        result = StringIO()
        pdf = pisa.pisaDocument(
            StringIO(html.encode("UTF-8")),
            result,
            encoding="utf-8")
                
        if pdf.err:
            return HttpResponse('Erro ao gerar pdf')

        resp = HttpResponse(result.getvalue(), mimetype='application/pdf')
        
        if name:
            resp['Content-Disposition'] = (
                'attachment; filename=%s' % name)

        return resp
        
