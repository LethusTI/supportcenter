# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Usado para atualizar a lista de municipios do brasil.'

    def handle(self, *args, **options):
        from lethusbox.municipios.utils import Loader
        print "Atualizando a lista de municipios"
        l = Loader()
        l.load()
