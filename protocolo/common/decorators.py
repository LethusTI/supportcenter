# -*- coding: utf-8 -*-

__all__ = ("json_response",)

from lethusbox.django.responses.json import JSONResponse

def json_response(f):
    
    def func(*args, **kwargs):
        return JSONResponse(f(*args, **kwargs))
    
    func.__name__ = f.__name__
    func.__doc__ = f.__doc__
    
    return func
