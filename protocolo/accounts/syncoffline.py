# -*- coding: utf-8 -*-

from social.apps.syncoffline.utils import SyncOfflineModule
from django.utils import simplejson as json
from social.apps.sync import sync_format, load_object
from models import *

class UserSyncOffline(SyncOfflineModule):
    def get_queryset(self, unidade, date):
        return User.objects
    
    def dump_object(self, obj):
        data = sync_format(obj)
        data['_type'] = type(obj).__name__

        return json.dumps(data)

    def load_object(self, pk, data):
        tp = data.get('_type')
        
        if tp == 'UnidadeProfile':
            cls_tp = UnidadeProfile
        elif tp == 'AdminProfile':
            cls_tp = AdminProfile
        elif tp == 'InstProfile':
            cls_tp = InstProfile
        else:
            return

        # Previne erro de username
        obj, created = cls_tp.objects.get_or_create(
            username=data['username'],
            auto_save=False)
        
        obj = load_object(cls_tp, pk, data, out_obj=obj)
        obj.save(cascade=False)

    class Meta:
        name = 'user'
        master = 'e' #Aceita apenas exportação
        slave = 'i' #Aceita apenas importação

class UnidadeGroupSyncOffline(SyncOfflineModule):
    def get_queryset(self, unidade, date):
        return UnidadeGroup.objects

    class Meta:
        name = "unidade_group"
        master = 'e' #Aceita apenas exportação
        slave = 'i' #Aceita apenas importação


class HistoricSyncOffline(SyncOfflineModule):
    def get_queryset(self, unidade, date):
        filter_kwargs = {}
        if unidade:
            filter_kwargs['unid'] = unidade

        if date:
            filter_kwargs['dtime__gte'] = date

        return Historic.objects(**filter_kwargs)


    def dump_object(self, obj):
        return json.dumps(sync_format(obj))

    def load_object(self, pk, data):
        obj = load_object(Historic, pk, data)
        obj.save(cascade=False)

    class Meta:
        name = "historic"
        master = 'i' #Aceita apenas importação
        slave = 'e' #Aceita apenas exportação
