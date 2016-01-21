# -*- coding: utf-8 -*-

import datetime
from dateutil.tz import tzlocal

import autocomplete_light
from django import forms
from django.utils.translation import ugettext as _

from weblobby import models

class RegistrosAddForm(forms.Form):
    datetime_formats = ['%d-%m-%Y %H:%M:%S',
                        '%d-%m-%Y %H:%M',
                        '%d-%m-%Y',
                        '%d/%m/%Y %H:%M:%S',
                        '%d/%m/%Y %H:%M',
                        '%d/%m/%Y',
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%d %H:%M',
                        '%Y-%m-%d',
                        '%Y/%m/%d %H:%M:%S',
                        '%Y/%m/%d %H:%M',
                        '%Y/%m/%d',
                        '%H:%M:%S %Y/%m/%d',
                        '%H:%M %Y/%m/%d',
                        '%H:%M:%S %Y-%m-%d',
                        '%H:%M %Y-%m-%d',
                        '%H:%M:%S %d/%m/%Y',
                        '%H:%M %d/%m/%Y',
                        '%H:%M:%S %d-%m-%Y',
                        '%H:%M %d-%m-%Y',]

    dataehora = forms.DateTimeField(label=_(u"Data e hora"), input_formats=datetime_formats, required=True)
    funcionario_contato_nome = forms.CharField(label=_(u"Funcionário contato"), widget=autocomplete_light.TextWidget('LdapUserAutocomplete'), required=False)
    setor_contato = forms.CharField(label=_(u"Setor contato"), widget=autocomplete_light.TextWidget('LdapGroupAutocomplete'), required=False)
    funcionario_matricula = forms.DecimalField(widget=forms.HiddenInput, required=False)
    observacao = forms.CharField(label=_(u"Observação"), max_length=300, required=False)
    entrada = forms.BooleanField(label=_(u"Entrada?"), required=False)

    visitante = None
    usuario = None

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['dataehora'].widget.attrs['class'] = 'date_time_input'
        self.fields['dataehora'].initial = datetime.datetime.now(tzlocal())

    def save(self, commit=True):
        instance = models.Registros()
        instance.visitante = self.visitante
        instance.usuario = self.usuario
        instance.dataehora = self.cleaned_data.get('dataehora')
        instance.entrada = self.cleaned_data.get('entrada')
        instance.observacao = self.cleaned_data.get('observacao')
        instance.funcionario_contato = self.cleaned_data.get('funcionario_matricula')
        instance.setor_contato = self.cleaned_data.get('setor_contato')

        if commit:
            instance.save()
        return instance

    class Media:
        js = ('js/profile.js',)