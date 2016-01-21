# -*- coding: utf-8 -*-

import autocomplete_light
import decimal
from base64 import b64decode

from localflavor.br import forms as formsbr
from django import forms
from django.forms import util
from django.utils.translation import ugettext as _
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from weblobby import models

class VisitanteFormSearch(forms.ModelForm):
    search = forms.CharField(label=_(u'Busca de visitantes'), required=False,
                             widget=autocomplete_light.TextWidget('VisitanteAutocomplete'))
    
    class Meta:
        model = models.Visitante
    
class VisitanteAddAndEditForm(forms.ModelForm):
    ESTADOS = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )
    
    cpf = formsbr.BRCPFField(label=_(u"CPF"), required=False)
    telefone = formsbr.BRPhoneNumberField(label=_(u"Telefone"), required=False)
    telefone_comercial = formsbr.BRPhoneNumberField(label=_(u"Telefone comercial"), required=False)
    uf = forms.ChoiceField(label=_(u'UF do emissor'), required=True, choices=ESTADOS, initial="-----")
    image_path = forms.CharField(label=_(u'Foto'), widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        cpf_invalid_message = _(u'CPF inválido.')
        cpf_max_digits_message = _(u'Esse campo aceita no mínimo 11 caracteres e no máximo 14.')
        cpf_digits_only_message = _(u'Esse campp aceita apenas números.')    
        telefone_invalid_message = _(u'O número de telefone deve seguir o seguinte formato: (XX) XXXXXXXX ou (XX) XXXXXXXXX')
        
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['telefone'].error_messages['invalid'] = telefone_invalid_message
        self.fields['telefone_comercial'].error_messages['invalid'] = telefone_invalid_message
        self.fields['cpf'].error_messages['invalid'] = cpf_invalid_message
        self.fields['cpf'].error_messages['max_digits'] = cpf_max_digits_message
        self.fields['cpf'].error_messages['digits_only'] = cpf_digits_only_message
    
    def clean_cpf(self):
        cpfstr = self.cleaned_data.get('cpf').replace('.', '').replace('-', '')
        if len(cpfstr) >= 1:
            cpfdec = decimal.Decimal(cpfstr)

            qtd = models.Visitante.objects.filter(cpf=cpfdec)

            # Se for edição não compara com ele mesmo
            if self.instance.pk is not None:
                qtd = qtd.exclude(pk=self.instance.pk)

            if qtd.count() >= 1:
                raise ValidationError(_(u'CPF já cadastrado.'))

            return cpfdec
        return None
    
    def clean_telefone(self):
        tel = self.cleaned_data.get('telefone').replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
        if len(tel) >= 1:
            return tel
        return None
    
    def clean_telefone_comercial(self):
        tel = self.cleaned_data.get('telefone_comercial').replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
        if len(tel) >= 1:
            return tel
        return None
    
    def clean_emissor(self):
        return self.cleaned_data.get('emissor').upper()
    
    def clean_image_path(self):
        rawdata = self.cleaned_data.get('image_path')
        
        if rawdata is None or rawdata == "":
            return rawdata

        # Por enquanto não permite editar a foto
        if self.instance.pk is not None:
            return rawdata
        
        try:
            image_data = b64decode(rawdata.split('base64,')[1])
        except:
            raise ValidationError(_(u'Imagem em formato inválido.'))
        
        return ContentFile(image_data, 'profile.jpeg')
    
    def validate_field(self, cleaned_data, field, message):
        if not cleaned_data.get(field) and self._errors.get(field) is None:
            self._errors[field] = util.ErrorList([message])
            return False
        return True
    
    def validate_wifi_fields(self, cleaned_data):
        message = _(u"Este campo é obrigatório para uso do Wi-Fi.")
        
        result = True
        if cleaned_data.get('wifi'):
            if not self.validate_field(cleaned_data, 'cpf', message):
                result = False
            if not self.validate_field(cleaned_data, 'email', message):
                result = False
            if not self.validate_field(cleaned_data, 'telefone', message):
                result = False
            if not self.validate_field(cleaned_data, 'telefone_comercial', message):
                result = False
        
        return result
    
    def validate_unique_together(self):
        if self.cleaned_data.get('passaporte'):
            qtd = models.Visitante.objects.filter(identidade=self.cleaned_data.get('identidade'),
                                                  passaporte=True)
        else:
            qtd = models.Visitante.objects.filter(identidade=self.cleaned_data.get('identidade'),
                                                  uf=self.cleaned_data.get('uf'),
                                                  emissor=self.cleaned_data.get('emissor'),
                                                  passaporte=False)

        if self.instance.pk is not None:
            qtd = qtd.exclude(pk=self.instance.pk)
        
        if qtd.count() >= 1:
            if self.cleaned_data.get('passaporte'):
                message = _(u'Passaporte %s já cadastrado.' % (self.cleaned_data.get('identidade')))
            else:
                message = _(u'Identidade %s-%s/%s já cadastrada.' % (self.cleaned_data.get('identidade'),
                                                                     self.cleaned_data.get('emissor'),
                                                                     self.cleaned_data.get('uf')))
            self._errors[NON_FIELD_ERRORS] = util.ErrorList([message])
            return False
        
        return True

    def clean(self):
        cleaned_data = self.cleaned_data

        passaporte = cleaned_data.get('passaporte')
        emissor = cleaned_data.get('emissor')

        if not passaporte:
            if emissor is None or emissor == '':
                self._errors['emissor'] = util.ErrorList([_(u'Este campo é obrigatório.')])
        else:
            cleaned_data['emissor'] = ''
            cleaned_data['uf'] = ''
        
        self.validate_wifi_fields(cleaned_data)
        self.validate_unique_together()
        
        return cleaned_data

    def __get_element_from_list(self, l, name):
        for item in l:
            if item == name:
                return item
        return False

    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)

        cleaned_cpf = self.cleaned_data.get('cpf')
        initial_cpf = self.initial.get('cpf')

        # Se mudou o CPF temos que deletar os atributos do CPF antigo.
        if cleaned_cpf != initial_cpf:
            instance.delete_all_attributes(instance.cpf_username(initial_cpf))

        if commit:
            instance.save()
        return instance

    def add_not_changed_message(self):
        self._errors[NON_FIELD_ERRORS] = util.ErrorList([_(u'Nenhuma alteração feita.')])
        
    class Meta:
        model = models.Visitante
        widgets = {
            'emissor': autocomplete_light.TextWidget('EmissorAutocomplete'),
            'empresa': autocomplete_light.TextWidget('EmpresaAutocomplete'),
        }