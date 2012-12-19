# -*- coding: utf-8 -*

__all__ = ('distribuitor',)

from protocolo import VERSION

CACHED_DISTRIBUITOR = {
    'VERSION': VERSION,
}

def distribuitor(request):
    return CACHED_DISTRIBUITOR
