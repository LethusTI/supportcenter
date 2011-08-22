#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lethusbox.django.responses.datatable import DataTableResponseMixin
from mongotools.views import MongoMultipleObjectMixin, ListView
from django.template import RequestContext
from lethusbox.django.output import render_to_csv, render_to_pdf

class HybridListView(DataTableResponseMixin, ListView, MongoMultipleObjectMixin):
    """
    Classe Hibrida
    que suporta paginas atraves da herança do MultipleObjectMixin
    que suporta saida em json tratada para o datatable
    atraves da herança do DataTableResponseMixin

    CVS: suporta a saida em cvs atraves do attributos:
    * csv_template_name -> template que sera usado para exportar
    * csv_template_filename -> arquivo de saida para csv

    que tambem é uma classe de vizualização do ListView
    """

    def post(self, request, *args, **kwargs):
        """
        ao invez de usarmos uma url para o action
        podemos reaproveitar o post do listview
        que esta livre
        """
        if not hasattr(self, 'action'):
            raise Http404

        act = self.action()
        return act.dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        # Look for a 'format=json' GET argument
        format = self.request.GET.get('format','html')

        if hasattr(self, "get_extra_context"):
            context.update(self.get_extra_context())

        if format == 'data':
            return DataTableResponseMixin.render_to_response(self, context)

        # Exportar para csv
        elif format == 'csv' and hasattr(self, "csv_template_name"):
            return render_to_csv(output = self.csv_filename,
                                 template = self.csv_template_name,
                                 context = context)

        # Exportar para pdf
        elif format == 'pdf' and hasattr(self, "pdf_template_name"):
            return render_to_pdf(output = self.pdf_filename,
                                 template = self.pdf_template_name,
                                 context = context)

        else:
            context['request'] = self.request

            return ListView.render_to_response(self,
                                               RequestContext(self.request, context))
