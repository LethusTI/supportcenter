# -*- coding: utf-8 -*-
__all__ = ('AdminSettingsForm')

from django.contrib.localflavor.br.forms import BRZipCodeField
       
import datetime

from PIL import Image, ImageOps

from lethusbox.municipios.models import MunicipioBrasil
from lethusbox.municipios.constants import UF_CHOICES

from django import forms
from mongotools.forms import MongoForm

from protocolo.common.fields import MyCepInput
from protocolo.common.models import SettingValue, ImageConstant

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
                                                            
class AdminSettingsForm(forms.Form):
    cidade = forms.CharField(max_length=200,
                             label="Cidade")
    uf = forms.ChoiceField(label="Estado",
                           choices=((('', '-----'),)+ UF_CHOICES))
    cep = BRZipCodeField(
        label="CEP",
        widget=MyCepInput(attrs={'class': 'cep'}))
    
    entidade = forms.CharField(max_length=300,
                               label=u"Nome completo da prefeitura")

    endr = forms.CharField(max_length=500,
                           label=u"Endereço da prefeitura",
                           widget=forms.Textarea)

    sec_name = forms.CharField(max_length=300,
                               label=u"Nome completo da secretaria responsável:",
                               initial=u"")
    
    brasao = forms.ImageField(
        label=u"Brasão do município",
        help_text="Carregue o brasão do município que será usado nos relatórios, memorandos, ofícios, etc",
        required=False)

    def __init__(self, *args, **kwargs):
        super(AdminSettingsForm, self).__init__(*args, **kwargs)

        self.initial['cidade'] = SettingValue.get('DEFAULT_CIDADE')
        self.initial['uf'] = SettingValue.get('DEFAULT_UF')
        self.initial['cep'] = SettingValue.get('DEFAULT_CEP')
        self.initial['entidade'] = SettingValue.get('DISTRIBUITOR_NAME')
        self.initial['endr'] = SettingValue.get('DISTRIBUITOR_ENDR')


        name = SettingValue.get('SEC_NAME')
        
        if name:
            self.initial['sec_name'] = name
    
    def clean_brasao(self):
        """
        Valida brasão para 80x80 e para JPG
        """
        data = self.cleaned_data['brasao']

        if not data:
            return

        img = Image.open(data)

        if (img.size[0] > 80 or img.size[1] > 80):
            img.thumbnail((80, 80), Image.ANTIALIAS)

        io = StringIO()
        img.save(io, 'JPEG')
        io.seek(0)

        return io
    
    def clean_social_url(self):
        if not self.cleaned_data.get('integrate_social', False):
            return

        data = self.cleaned_data['social_url']

        if not data:
            raise forms.ValidationError(u'Por favor informe a url que está instalado o lethus-social')

        try:
            uo = urllib.urlopen('%ssaude-webservice/?cmd=get_information' % data)
            json_data = json.loads(uo.read())
        except:
            raise forms.ValidationError(u'Servidor Lethus social inválido')
        else:
            if json_data.get('name') != 'Lethus social':
                raise forms.ValidationError(u'O Servidor informado não provê o Lethus social')

        return data

    def save(self, *args, **kwargs):
        if self.cleaned_data.get('brasao'):
            ImageConstant.set('brasao', self.cleaned_data['brasao'])

        SettingValue.set('DEFAULT_CIDADE', self.cleaned_data['cidade'])
        SettingValue.set('DEFAULT_UF', self.cleaned_data['uf'])
        SettingValue.set('DEFAULT_CEP', self.cleaned_data['cep'])
        SettingValue.set('SEC_NAME', self.cleaned_data['sec_name'])
        SettingValue.set('DISTRIBUITOR_NAME', self.cleaned_data['entidade'])
        SettingValue.set('DISTRIBUITOR_ENDR', self.cleaned_data['endr'])


