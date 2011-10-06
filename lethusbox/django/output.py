from django.template import loader, Context
from django.http import HttpResponse
from django.template import RequestContext
from ho import pisa
import cStringIO as StringIO
import cgi
from django.conf import settings
from django.contrib.staticfiles.finders import find

def render_to_csv(output, template, context):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = ('attachment; filename=%s' %
                                       output)
            
    t = loader.get_template(template)
    response.write(t.render(Context(context)))
    return response

def fetch_resources(uri, rel):
    if uri.startswith('/static'):
        uri = uri.replace('/static/', '')
        if settings.DEBUG:
            return find(uri)
        else:
            return os.path.join(settings.STATIC_ROOT, uri)
            

def render_to_pdf(output, template, context, request=None):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = ('attachment; filename=%s' %
                                       output)
            
    t = loader.get_template(template)

    if request:
        c = RequestContext(request, context)
    else:
        c = Context(context)

    html  = t.render(c)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(
        StringIO.StringIO(
            html.encode("UTF-8")), result,
        link_callback=fetch_resources)

    if not pdf.err:
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = ('attachment; filename=%s' %
                                       output)

        response.write(result.getvalue())
        return response

    return HttpResponse('Gremlins ate your pdf! %s' % cgi.escape(html))
