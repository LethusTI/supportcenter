# -*- coding: utf-8 -*

__all__ = ('BairroForm', 'EnderecoForm', 'EndrSelectForm')

from django import forms
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from mongotools.forms import MongoForm
from lethusbox.municipios.models import MunicipioBrasil
from lethusbox.django.fields import IdChoiceField

from models import *

class BairroForm(MongoForm):
    uf = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=(('', ''),) + STATE_CHOICES)

    mun = IdChoiceField(
        label="Município",
        required=True)

    distrito_nome = forms.CharField(
        label="Distrito",
        required=False,
        max_length=150)

    distrito_select = IdChoiceField(
        label="Distrito",
        required=False)

    def __init__(self, *args, **kwargs):
        super(BairroForm, self).__init__(*args, **kwargs)

        if self.data and self.data.get('uf'):
            self._fill_uf(self.data['uf'])
        elif self.instance and self.instance.mun:
            mun_obj = self.instance.mun_obj

            self.initial['uf'] = mun_obj.uf_sigla
            self._fill_uf(mun_obj.uf_sigla)
            self.initial['mun'] = mun_obj.codigo

            self._fill_mun(mun_obj.codigo)

        if self.instance and self.instance.distrito:
            self.initial['distrito_select'] = self.instance.distrito.codigo

    def clean_mun(self):
        _id = self.cleaned_data['mun']

        obj = MunicipioBrasil.objects.with_id(_id)

        if not obj:
            raise forms.ValidationError("Município inválido")

        return obj

    def clean_distrito_select(self):
        _id = self.cleaned_data['distrito_select']

        if not _id:
            return

        obj = Distrito.objects.with_id(_id)

        if not obj:
            raise forms.ValidationError(u'Distrito inválido')
        
        return obj


    def _fill_uf(self, uf):
        """
        Preenche o UF
        """
        self.fields['mun'].choices = [('', '')] + [
            (m.codigo, m.nome)
            for m in MunicipioBrasil.objects(uf_sigla=uf).order_by('nome')]

    def _fill_mun(self, mun):
        """
        Preenche o municipio
        """
        self.fields['distrito_select'].choices = [('', '')] + [
            (d.codigo, d.nome)
            for d in Distrito.objects(mun=mun).order_by('nome')]
    

    def save(self, *args, **kwargs):
        obj = super(BairroForm, self).save(commit=False)
        obj.mun = self.cleaned_data['mun'].codigo

        if self.cleaned_data.get('distrito_select', None):
            obj.distrito = self.cleaned_data['distrito_select']
        elif self.cleaned_data.get('distrito_nome'):
            dst_nome = self.cleaned_data['distrito_nome']

            dst = Distrito.objects(
                mun=obj.mun,
                nome=dst_nome).first()

            if not dst:
                dst = Distrito(
                    nome=dst_nome,
                    mun=obj.mun)
                dst.save()

            obj.distrito = dst

        if kwargs.get('commit', True):
            obj.save()

        return obj
        
    class Meta:
        document = Bairro
        fields = ('nome',)

    class Media:
        js = ('js/bootstrap-combobox.js',
              'js/bootstrap-relationbox.js',
              'js/bairro.form.js')

        css = {
            'all': ('css/bootstrap-combobox.css',
                    'css/bairro.form.css')
            }

class EnderecoForm(MongoForm):
    uf = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=(('', ''),) + STATE_CHOICES)

    mun = IdChoiceField(
        label="Município",
        required=True)

    distrito = IdChoiceField(
        label="Distrito",
        required=False)

    bairro = IdChoiceField(
        label="Bairro",
        required=False)

    def __init__(self, *args, **kwargs):
        super(EnderecoForm, self).__init__(*args, **kwargs)

        self.fields['log'].widget.attrs.update({'class': 'log'})
        self.fields['cep'].widget.attrs.update({'class': 'cep'})
        self.fields['num'].widget.attrs.update({'class': 'num'})

        if self.data:
            if self.data.get(self.add_prefix('uf')):
                self._fill_uf(self.data[self.add_prefix('uf')])

            if self.data.get(self.add_prefix('mun')):
                self._fill_mun(self.data[self.add_prefix('mun')])

            if self.data.get(self.add_prefix('distrito')):
                self._fill_distrito_id(self.data[self.add_prefix('distrito')])

        elif self.instance:
            if self.instance.mun:
                mun_obj = self.instance.mun_obj

                self.initial['uf'] = mun_obj.uf_sigla
                self._fill_uf(mun_obj.uf_sigla)
                self.initial['mun'] = mun_obj.codigo

                self._fill_mun(mun_obj.codigo)

            if self.instance.distrito:
                self.initial['distrito'] = self.instance.distrito.codigo
                self._fill_distrito_id(self.instance.distrito.codigo)

    def _fill_uf(self, uf):
        """
        Preenche o UF
        """
        self.fields['mun'].choices = [('', '')] + [
            (m.codigo, m.nome)
            for m in MunicipioBrasil.objects(uf_sigla=uf).order_by('nome')]

    def _fill_mun(self, mun):
        """
        Preenche o municipio
        """
        self.fields['distrito'].choices = [('', '')] + [
            (d.codigo, d.nome)
            for d in Distrito.objects(mun=int(mun)).order_by('nome')]

        self.fields['bairro'].choices = [('', '')] + [
            (b.codigo, b.nome)
            for b in Bairro.objects(
                mun=int(mun),
                distrito=None).order_by('nome')]

    def _fill_distrito_id(self, dst_id):
        """
        Preenche o distrito
        """
        self.fields['bairro'].choices = [('', '')] + [
            (b.codigo, b.nome)
            for b in Bairro.objects(
                distrito=int(dst_id)).order_by('nome')]

    def clean_mun(self):
        pk = self.cleaned_data['mun']

        if not pk:
            return

        obj = MunicipioBrasil.objects.with_id(pk)

        if not obj:
            raise forms.ValidationError(u"Município inválido")

        return obj

    def clean_distrito(self):
        pk = self.cleaned_data['distrito']

        if not pk:
            return

        obj = Distrito.objects.with_id(pk)

        if not obj:
            raise forms.ValidationError(u"Distrito inválido")

        return obj

    def clean_bairro(self):
        pk = self.cleaned_data['bairro']

        if not pk:
            return

        obj = Bairro.objects.with_id(pk)

        if not obj:
            raise forms.ValidationError(u"Bairro inválido")

        return obj

    def save(self, *args, **kwargs):
        obj = super(EnderecoForm, self).save(commit=False)

        obj.distrito = self.cleaned_data['distrito']
        obj.bairro = self.cleaned_data['bairro']
        obj.mun = self.cleaned_data['mun'].codigo

        if kwargs.get('commit', True):
            obj.save()

        return obj

    class Meta:
        document = Endereco
        exclude = ('mun',)

    class Media: 
        js = ('js/bootstrap-combobox.js',
              'js/bootstrap.municipio_completion.js',
              'js/endr.form.js')

        css = {
            'all': ('css/endr.form.css',
                    'css/bootstrap-combobox.css')
              }

class EndrSelectForm(forms.Form):
    uf = forms.ChoiceField(
        label="Estado",
        required=True,
        choices=(('', ''),) + STATE_CHOICES)

    mun = IdChoiceField(
        label="Município",
        required=True)

    distrito = IdChoiceField(
        label="Distrito",
        required=False)

    bairro = IdChoiceField(
        label="Bairro",
        required=False)

    def __init__(self, data=None, allow_defaults=True, *args, **kwargs):
        super(EndrSelectForm, self).__init__(data, *args, **kwargs)
        

    def clean_mun(self):
        pk = self.cleaned_data['mun']

        if not pk:
            return

        obj = MunicipioBrasil.objects.with_id(pk)

        if not obj:
            raise forms.ValidationError(u"Município inválido")

        return obj

    def clean_distrito(self):
        pk = self.cleaned_data['distrito']

        if not pk:
            return

        obj = Distrito.objects.with_id(pk)

        if not obj:
            raise forms.ValidationError(u"Distrito inválido")

        return obj

    def clean_bairro(self):
        pk = self.cleaned_data['bairro']

        if not pk:
            return

        obj = Bairro.objects.with_id(pk)

        if not obj:
            raise forms.ValidationError(u"Bairro inválido")

        return obj
