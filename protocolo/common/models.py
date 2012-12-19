# -*- coding: utf-8 -*-

__all__ = ('SettingValue')

import datetime
import re

from mongoengine import *

from lethusbox.municipios.models import MunicipioBrasil
from lethusbox.municipios.constants import UF_CHOICES
from .constants import *

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.core.files.temp import NamedTemporaryFile
#from hurry.filesize import size
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.utils.safestring import mark_safe


PHOTO_MIMETYPES = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'JPG': 'image/jpeg',
    'GIF': 'image/gif',
    #TODO: se encontrar mais coloque aqui
}

class PhotoAlbum(Document):
    image = ImageField(
        db_alias='fs', #database especial para arquivos
        size=(800, 600),
        thumbnail_size=(160, 120, False))
    locked = BooleanField(default=False)
    comment = StringField(max_length=200)
    created = DateTimeField(default=datetime.datetime.now)
    album = ReferenceField('Album')

    @property
    def mimetype(self):
        return PHOTO_MIMETYPES.get(self.image.format)

    def as_response(self):
        wrapper = FileWrapper(self.image)
        response = HttpResponse(wrapper, content_type=self.mimetype)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response['Expires'] = 'Sat, 26 Jul 1997 05:00:00 GMT'
        response['Pragma'] = 'no-cache'
        return response

    def json_format(self):
        return {
            'pk': str(self.pk),
            'comment': self.comment
            }

    def as_thumb_response(self):
        wrapper = FileWrapper(self.image.thumbnail)
        response = HttpResponse(wrapper, content_type=self.mimetype)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response['Expires'] = 'Sat, 26 Jul 1997 05:00:00 GMT'
        response['Pragma'] = 'no-cache'
        
        return response

    def delete(self, force=False, *args, **kwargs):
        if self.locked and not force:
            return

        self.image.delete() #apaga a imagem do banco de dados
        return super(PhotoAlbum, self).delete(*args, **kwargs)

    meta = {'allow_inheritance': False,
            'collection': 'album_photo',
            'ordering': ['created'],
            'indexes': [
               {'fields': ['album', 'created']},
               {'fields': ['created']},
            ]}


class SettingValue(Document):
    """
    Usado para guardar as configurações do sistema
    """
    key = StringField(primary_key=True)
    value = StringField()

    _dict_cache = None
    meta = {'allow_inheritance': False,
            'collection': 'settings'}

    @classmethod
    def as_dict(cls):
        return dict(list(cls.objects.scalar('key', 'value')))

    @classmethod
    def get(cls, key, default=None):
        if cls._dict_cache is None:
            cls._dict_cache = cls.as_dict()

        return cls._dict_cache.get(key, default)

    @classmethod
    def set(cls, key, value):
        if cls._dict_cache:
            cls._dict_cache[key] = value

        obj = cls(key=key, value=value)
        obj.save()

        return obj


    @classmethod
    def get_bool(cls, key, default=None):
        v = cls.get(key, default)

        if v == 'true':
            return True

        elif v == 'false':
            return False


    @classmethod
    def set_bool(cls, key, value):
        if value == True:
            v = 'true'
        elif value == False:
            v = 'false'
        else:
            v = None

        cls.set(key, v)

class ImageConstant(Document):
    """
    Utilizado para guardar imagens que são constantes
    ex como brasões logos, etc
    """
    _cache = {}
    _open_images = {}

    key = StringField(primary_key=True)
    image = ImageField(
        db_alias='fs') #database especial para arquivos

    meta = {'allow_inheritance': False,
            'collection': 'image_constant'}

    @classmethod
    def set(cls, key, bf):
        old = cls.objects.with_id(key)

        if old:
            old.delete()
        
        #Cache
        cls.reset_cache(key)

        obj = cls(key=key)
        obj.image.put(bf)
        obj.save()

        return obj

    @classmethod
    def has(cls, key):
        return cls.objects(key=key).count() > 0

    def delete(self,  *args, **kwargs):
        self.image.delete() #apaga a imagem do banco de dados
        return super(ImageConstant, self).delete(*args, **kwargs)

    @classmethod
    def get(cls, key):
        obj = cls.objects.with_id(key)

        if not obj:
            return

    @classmethod
    def get_cached(cls, key):
        if not cls._cache.has_key(key):
            obj = ImageConstant.objects.with_id(key)

            if not obj:
                return

            f = NamedTemporaryFile(
                delete=False,
                suffix='.%s' % obj.image.format)

            buf = obj.image.read()

            if not buf:
                return

            f.write(buf)
            cls._open_images[key] = f
            
            f.flush()

            cls._cache[key] = f.name
        
        return cls._cache[key]

    @classmethod
    def reset_all_cache(cls):
        cls._cache = {}
        cls._open_images = {}

    @classmethod
    def reset_cache(cls, key):
        if cls._cache.has_key(key):
            del cls._cache[key]

        if cls._open_images.has_key(key):
            del cls._open_images[key]


