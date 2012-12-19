# -*- coding: utf-8 -*-

def get_group_choices(choices):
    """
    usado para simplificar as choices em grupo
    retorna em dict formato simples
    """
    out = {}

    def find(choices):
        for k, v in choices:
            if isinstance(v, tuple):
                find(v)
            else:
                out[k] = v
        
    find(choices)
    return out
