# -*- coding: utf-8 -*-

VERSION = "0.9.0dev"

import sys
import os
preloaded_models = set()

def setup_paths():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    sys.path.insert(0, os.path.join(BASE_DIR, 'packages'))
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.dirname(BASE_DIR))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def preload_models():
    from django.conf import settings
    from django.utils.importlib import import_module

    for app_name in settings.INSTALLED_APPS:
        app_module = import_module(app_name)

        try:
            models = import_module('.models', app_name)
        except ImportError:
            continue
        
        preloaded_models.add(models)
        
def connect_db():
    from mongoengine import register_connection
    from django.conf import settings

    if hasattr(settings, "MONGODB_DATABASES"):
        databases = settings.MONGODB_DATABASES
    else:
        databases = {}
        db_name = getattr(settings, "MONGODB_DATABASE", "supportcenter")
        host = getattr(settings, "MONGODB_HOST", None)
        port = getattr(settings, "MONGODB_PORT", None)
        username = getattr(settings, "MONGODB_USERNAME", None)
        password = getattr(settings, "MONGODB_PASSWORD", None)

        d = {'NAME': db_name}
        if host:
            d['HOST'] = host
        if port:
            d['PORT'] = port
        if username:
            d['USERNAME'] = username
        if password:
            d['PASSWORD'] = password
        databases['default'] = d

        for alias in ('fs', 'tmp', 'log'):
            d = {'NAME': db_name+alias}
            if host:
                d['HOST'] = host
            if port:
                d['PORT'] = port
            if username:
                d['USERNAME'] = username
            if password:
                d['PASSWORD'] = password

            databases[alias] = d

    for alias, db in databases.iteritems():
        kwargs = {}
        kwargs['name'] = db.get('NAME')
        
        if db.get('HOST'):
            kwargs['host'] = db['HOST']
            
        if db.get('PORT'):
            kwargs['port'] = db['PORT']

        if db.get('USERNAME'):
            kwargs['username'] = db['USERNAME']

        if db.get('PASSWORD'):
            kwargs['password'] = db['PASSWORD']
        
        register_connection(alias, **kwargs)
        
    preload_models()
