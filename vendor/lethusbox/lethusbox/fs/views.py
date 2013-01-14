# -*- coding: utf-8 -*-

__all__ = ('FileViewMixIn', 'FileUploadMixIn')

from mongoengine.django.shortcuts import get_document_or_404
from lethusbox.django.decorators import json_response

from .models import *

class FileViewMixIn(object):
    """
    MixIn para View que permite o download de arquivos de alguma pasta.
    """
    def get_folder(self):
        """
        Para implementar nas classes mixadas. é usada para retornar a pasta de arquivos que haverá operações.
        """
        raise NotImplementedError

    def _get_file(self, pk):
        folder = self.get_folder()
        f = get_document_or_404(folder.files, pk=pk)
        return f.as_response()

    def get(self, *args, **kwargs):
        f = self.request.GET.get('get_file')

        if f:
            return self._get_file(f)

        return super(FileViewMixIn, self).get(*args, **kwargs)
    
class FileUploadMixIn(FileViewMixIn):
    """
    Filha de FileViewMixIn.
    
    MixIn para View que permite o download e o envio de arquivos de/para alguma pasta.
    
    Implementar todos os metodos em requisito de sua classe pai.
    """
    @json_response
    def _delete_file(self, pk):
        folder = self.get_folder()
        f = get_document_or_404(folder.files, pk=pk)
        f.delete()

        return {'deleted': True}

    @json_response
    def _post_file(self):
        folder = self.get_folder()
        infile = self.request.FILES.get('file')

        if infile:
            file = folder.put_file(infile,
                                   filename=infile.name,
                                   content_type=infile.content_type)
            return file.json_format()
        else:
            return {'error': "Informe o arquivo a ser enviado"}

    def post(self, *args, **kwargs):
        """
        Para enviar uma foto
        """
        pk = self.request.POST.get('delete_file')
        if pk:
            return self._delete_file(pk)

        cmd = self.request.POST.get('cmd')
        if cmd == 'post_file':
            return self._post_file()

        return super(FileUploadMixIn, self).post(*args, **kwargs)

class PhotoViewMixIn(object):
    """
    MixIn de View para visualização de fotos de um álbum.
    """
    def get_album(self):
        """
        Implementação obrigatória na classe mixada.
        deve retornar o albúm que haverá operações.
        """
        raise NotImplementedError #implementar na classe filha

    def _view_photo(self, pk):
        album = self.get_album()
        photo = get_document_or_404(album.photos, pk=pk)
        return photo.as_response()

    def _view_thumb(self, pk):
        album = self.get_album()
        photo = get_document_or_404(album.photos, pk=pk)

        return photo.as_thumb_response()

    def get(self, *args, **kwargs):
        photo = self.request.GET.get('view_photo')
        thumb = self.request.GET.get('view_thumbnail')
        
        if photo:
            return self._view_photo(photo)

        if thumb:
            return self._view_thumb(thumb)

        return super(PhotoViewMixIn, self).get(*args, **kwargs)


class PhotoUploadMixIn(PhotoViewMixIn):
    """
    Filha de PhotoViewMixIn.

    MixIn para View que permite a visualização e o envio de fotos para um álbum.

    implementar todos os metodos da classe pai.
    """
    @json_response
    def _delete_photo(self, pk):
        album = self.get_album()
        photo = get_document_or_404(album.photos, pk=pk)

        if photo.locked:
            return {'error': u"As imagens adicionadas não podem mais ser removidas"}

        photo.delete()

        return {'deleted': True}

    @json_response
    def _edit_photo(self, pk):
        album = self.get_album()
        photo = get_document_or_404(album.photos, pk=pk)

        photo.comment = self.request.POST.get('comment')
        
        try:
            photo.save()
        except ValidationError, e:
            return {'error': "Comentário inválido"}
        else:
            return photo.json_format()

    @json_response
    def _post_photo(self):
        album = self.get_album()
        infile = self.request.FILES.get('file')
    
        if infile:
            photo = album.put_file(infile)
            return photo.json_format()
        else:
            return {'error': "Informe o arquivo a ser enviado"}

    def post(self, *args, **kwargs):
        """
        Para enviar uma foto
        """
        pk = self.request.POST.get('delete_photo')
        if pk:
            return self._delete_photo(pk)

        pk = self.request.POST.get('edit_photo')
        if pk:
            return self._edit_photo(pk)

        cmd = self.request.POST.get('cmd')
        if cmd == 'post_photo':
            return self._post_photo()

        return super(PhotoUploadMixIn, self).post(*args, **kwargs)
