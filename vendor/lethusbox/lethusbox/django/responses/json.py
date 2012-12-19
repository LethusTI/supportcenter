from django.utils import simplejson as json
from django.http import HttpResponse

class JSONResponse(HttpResponse):
    """ JSON response class """
    def __init__(self,content='',json_opts={},mimetype="application/json; charset=utf-8",*args,**kwargs):
        
        if content:
            content = json.dumps(content,**json_opts)
        else:
            content = json.dumps([],**json_opts)

        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
