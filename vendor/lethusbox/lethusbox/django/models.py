# -*- coding: utf-8 -*-

__all__ = ('SettingValue', 'ImageConstant')

from mongoengine import *
from django.core.files.temp import NamedTemporaryFile

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
    def get_uncached(cls, key, default=None):
        """
        Busca valores do banco sem consultar o cache
        """
        obj = cls.objects(key=key).first()

        if obj:
            return obj.value

        return default

    @classmethod
    def unset(cls, key):
        """
        Remove uma configuração do banco de dados

        key: chave única da configuração para ser removida.
        """
        if cls._dict_cache:
            if cls._dict_cache.has_key(key):
                del cls._dict_cache[key]

        cls.objects(key=key).delete()

    @classmethod
    def set(cls, key, value):
        """
        Guarda uma configuração.

        * key: nome único da configuração.
        * value: valor para ser definido.
        """
        if cls._dict_cache:
            cls._dict_cache[key] = value

        obj = cls(key=key, value=value)
        obj.save()

        return obj


    @classmethod
    def get_bool(cls, key, default=None):
        """
        Busca valores booleanos gravados

        * key: chave da configuração
        * default: se não encontrar retorne.
        """
        v = cls.get(key, default)

        if v == 'true':
            return True

        elif v == 'false':
            return False

        return default

    @classmethod
    def set_bool(cls, key, value):
        """
        Guarda uma configuração booleana

        * key: chave da configuração.
        * value: valor True, False ou None
        """
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
        """
        Seta uma imagem costante
        
        * key: chave da imagem
        * buf: buffer contendo a imagem
        """
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
        """
        Retorna verdadeiro se possui a imagem no banco de dados.

        * key: chave da imagem
        """
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
        """
        Busca imagem no cache, se não encontrada tenta buscar no banco de dados.

        * key: chave da imagem
        """
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
        """
        Limpa todo cache
        """
        cls._cache = {}
        cls._open_images = {}

    @classmethod
    def reset_cache(cls, key):
        """
        Limpa o cache de uma imagem
        
        * key: chave da imagem
        """
        if cls._cache.has_key(key):
            del cls._cache[key]

        if cls._open_images.has_key(key):
            del cls._open_images[key]

