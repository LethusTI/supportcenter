from django.template import loader, Context
from django.http import HttpResponse
from ho import pisa
import cStringIO as StringIO
import cgi

def render_to_csv(output, template, context):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = ('attachment; filename=%s' %
                                       output)
            
    t = loader.get_template(template)
    response.write(t.render(Context(context)))
    return response

def render_to_pdf(output, template, context):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = ('attachment; filename=%s' %
                                       output)
            
    t = loader.get_template(template)
    html  = t.render(Context(context))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = ('attachment; filename=%s' %
                                       output)

        response.write(result.getvalue())
        return response

    return HttpResponse('Gremlins ate your pdf! %s' % cgi.escape(html))
