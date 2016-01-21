# -*- coding: utf-8 -*-

import autocomplete_light
from django.utils.translation import ugettext_lazy as _

from weblobby.ldap import LdapUser
from weblobby.ldap import LdapGroup
from weblobby.models import Visitante

class WeblobbyAutocompleteBase(autocomplete_light.AutocompleteBase):
    limit_choices = 20
    html_notfound_message = _('Nenhuma entrada encontrada')

    def __get_key(self, obj):
        return obj

    def order_choices(self, choices):
        return sorted(choices, key=self.__get_key, reverse=False)

    def choices_for_values(self):
        return self.order_choices(self.values)

    def autocomplete_html(self):
        html = ''.join(
            [self.choice_html(c) for c in self.choices_for_request()])

        if not html:
            html = self.empty_html_format % self.html_notfound_message

        return self.autocomplete_html_format % html

class EmissorAutocomplete(WeblobbyAutocompleteBase):
    autocomplete_js_attributes = {'placeholder': _('Busca emissor'), 'minimum_characters': 1,}
    html_notfound_message = _('Nenhum emissor encontrado')

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude')
        visitantes = Visitante.objects.filter(emissor__icontains=q).exclude(emissor__icontains=exclude).distinct('emissor')[0:self.limit_choices]
        emissores = []
        for v in visitantes:
            emissores.append(v.emissor)
        self.choices = emissores
        return self.order_choices(self.choices)

class EmpresaAutocomplete(WeblobbyAutocompleteBase):
    autocomplete_js_attributes = {'placeholder': _('Busca empressa'), 'minimum_characters': 2,}
    html_notfound_message = _('Nenhuma empressa encontrada')

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude')
        visitantes = Visitante.objects.filter(empresa__icontains=q).exclude(empresa__icontains=exclude).distinct('empresa')[0:self.limit_choices]
        empresas = []
        for v in visitantes:
            empresas.append(v.empresa)
        self.choices = empresas
        return self.order_choices(self.choices)

class LdapUserAutocomplete(WeblobbyAutocompleteBase):
    limit_choices = 10
    autocomplete_js_attributes = {'placeholder': 'Busca funcionário contato', 'minimum_characters': 3,}
    html_notfound_message = 'Nenhuma contato encontrado'

    def __get_key(self, obj):
        return obj.displayname

    def choices_for_request(self):
        q = self.request.GET.get('q', '')

        users = LdapUser.objects.filter(displayname__icontains=q)[0:self.limit_choices]
        users_filtered = []
        for u in users:
            if u.employeenumber is not None and u.employeenumber != '':
                users_filtered.append(u)
        self.choices = users_filtered
        return self.order_choices(self.choices)

    def choice_value(self, choice):
        return choice.employeenumber

class LdapGroupAutocomplete(WeblobbyAutocompleteBase):
    limit_choices = 10
    autocomplete_js_attributes = {'placeholder': 'Busca setor contato', 'minimum_characters': 2,}
    html_notfound_message = 'Nenhuma contato encontrado'

    def __get_key(self, obj):
        return obj.cn

    def choices_for_request(self):
        q = self.request.GET.get('q', '')

        self.choices = LdapGroup.objects.filter(cn__icontains=q)[0:self.limit_choices]
        return self.order_choices(self.choices)

autocomplete_light.register(EmissorAutocomplete)
autocomplete_light.register(EmpresaAutocomplete)
autocomplete_light.register(LdapUserAutocomplete)
autocomplete_light.register(LdapGroupAutocomplete)

autocomplete_light.register(Visitante, search_fields=('nome', 'identidade', 'emissor', 'uf', 'cpf', 'id',),
                            autocomplete_js_attributes={'placeholder': 'Busca de visitante', 'minimum_characters': 2,})