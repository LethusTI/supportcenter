# -*- coding: utf-8 -*-

__all__ = ('Folder', 'FileFolder', 'Album', 'PhotoAlbum')

import datetime
from mongoengine import *
from bson import ObjectId

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from filesize import size

PHOTO_MIMETYPES = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'JPG': 'image/jpeg',
    'GIF': 'image/gif',
    #TODO: se encontrar mais coloque aqui
}

class Album(Document):
    """
    Classe que representa um álbum.

    Atributos:
    
    * ref: referência para o documento dono do álbum
    * created: data de criação do álbum
    """
    ref = GenericReferenceField() # documento dono do album
    created = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def new_from_owner(cls, owner):
        """
        Cria um novo album para um objeto
        """
        obj = cls(ref=owner)
        obj.save()

        return obj

    @property
    def photos(self):
        """
        Retorna uma queryset das fotos do álbum
        """
        return PhotoAlbum.objects(album=self)

    def put_file(self, infile, pk=None):
        """
        Insere uma foto no album

        * infile: arquivo do tipo IO de entrada.
        * pk: para definir uma chave primaria para foto (não obrigatório).
        """
        photo = PhotoAlbum()
        photo.image.put(infile)
        photo.album = self

        if pk:
            photo.pk = ObjectId(pk)

        photo.save()

        return photo

    def delete_all_photos(self):
        """
        Remove todas as fotos do álbum
        """
        for photo in self.photos:
            photo.delete()

    def delete(self, *args, **kwargs):
        """
        Apaga o album e suas fotos
        """
        self.delete_all_photos()
        return super(Album, self).delete(*args, **kwargs)

    
    def lock_photos(self):
        """
        Tranca as fotos para proibir a remoção.
        """
        for photo in self.photos:
            photo.locked = True
            photo.save()

    meta = {'allow_inheritance': False,
            'collection': 'album',
            'indexes': [
               {'fields': ['ref']},
            ]}

class PhotoAlbum(Document):
    """
    Representa uma foto de um álbum.

    Atributos:

    * image: ImageField para armazenar a imagem tamanho máximo 800x600, thumbnail de 160x120.
    
    * locked: se a foto está tracada para remoção/edição.

    * comment: comentário da foto.
    * created: data e hora de criação da foto
    * album: álbum referênte da foto.
    """
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
        """
        Retorna a resposta HTTP contento a imagem
        """
        wrapper = FileWrapper(self.image)
        response = HttpResponse(wrapper, content_type=self.mimetype)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response['Expires'] = 'Sat, 26 Jul 1997 05:00:00 GMT'
        response['Pragma'] = 'no-cache'
        return response

    def json_format(self):
        """
        Retorna em formato JSON para re-envio.
        """
        return {
            'pk': str(self.pk),
            'comment': self.comment
            }

    def as_thumb_response(self):
        """
        Retorna a resposta HTTP contento a imagem em thumbnail.
        """
        wrapper = FileWrapper(self.image.thumbnail)
        response = HttpResponse(wrapper, content_type=self.mimetype)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response['Expires'] = 'Sat, 26 Jul 1997 05:00:00 GMT'
        response['Pragma'] = 'no-cache'
        
        return response

    def delete(self, force=False, *args, **kwargs):
        """
        Deleta a imagem do banco de dados.
        """
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

class FileFolder(Document):
    """
    Representa um arquivo de uma pasta.
    """
    file = FileField(db_alias='fs') #database especial para arquivos
    created = DateTimeField(default=datetime.datetime.now)
    folder = ReferenceField('Folder')

    @property
    def mimetype(self):
        return getattr(self.file, 'content_type')

    @property
    def filename(self):
        """
        Retorna o nome do arquivo
        """
        return getattr(self.file, 'name')

    @property
    def size(self):
        """
        Retorna o tamanho em bytes do arquivo.
        """
        return getattr(self.file, 'length')
    
    @property
    def human_size(self):
        """
        Retorna o tamanho humanizado do arquivo
        """
        return size(self.size)

    def json_format(self):
        """
        Retorna o arquivo em formato JSON
        """
        return {
            'pk': str(self.pk),
            'filename': self.filename,
            'human_size': self.human_size
            }
    
    def as_response(self):
        """
        Retorna resposta HTTP contendo o arquivo anexado.
        """
        wrapper = FileWrapper(self.file)
        response = HttpResponse(wrapper, content_type=self.mimetype)
        response['Content-Disposition'] = (
            u'attachment; filename=%s' % self.filename).encode('utf8')
        response['Cache-Control'] = 'no-cache'
        return response

    def delete(self, *args, **kwargs):
        """
        Remove o arquivo do banco de dados.
        """
        self.file.delete() #apaga a imagem do banco de dados
        return super(FileFolder, self).delete(*args, **kwargs)

    meta = {'allow_inheritance': False,
            'collection': 'file_folder',
            'ordering': ['created'],
            'indexes': [
               {'fields': ['folder', 'created']},
               {'fields': ['created']},
            ]}

class Folder(Document):
    """
    Representa uma pasta de arquivos.
    
    Atributos:
    
    * ref: referência para o documento dono da pasta
    * created: data e hora de criação da pasta
    """
    ref = GenericReferenceField() # documento dono da pasta
    created = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def new_from_owner(cls, owner):
        """
        Cria uma pasta para um objeto
        """
        obj = cls(ref=owner)
        obj.save()

        return obj

    @property
    def files(self):
        """
        Retorna os arquivos contidos na pasta
        """
        return FileFolder.objects(folder=self)

    def put_file(self, infile, **kwargs):
        """
        Insere um arquivo na pasta
        """
        f = FileFolder()
        f.file.put(infile, **kwargs)
        f.folder = self
        f.save()

        return f

    def delete(self, *args, **kwargs):
        """
        Apaga a pasta e seus arquivos
        """
        for f in self.files:
            f.delete()

        return super(Folder, self).delete(*args, **kwargs)

    meta = {'allow_inheritance': False,
            'collection': 'folder',
            'indexes': [
               {'fields': ['ref']},
            ]}

