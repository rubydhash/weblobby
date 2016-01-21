# -*- coding: utf-8 -*-

__author__ = 'jimmy'

import datetime
import string
import random
from os import path

from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth.models import User

from weblobby import radius
from weblobby import util
from weblobby.ldap import LdapUser

class Visitante(models.Model):
    id = util.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)
    identidade = models.CharField(max_length=100, blank=False, verbose_name=_(u"Nº/Identidade"))
    emissor = models.CharField(max_length=10, blank=True, verbose_name=_(u"Emissor (Sigla)"))
    uf = models.CharField(max_length=3, blank=True, verbose_name=_(u"UF do emissor"))
    passaporte = models.BooleanField(null=False, blank=False, default=False)
    empresa = models.CharField(max_length=100, blank=False)

    wifi = models.BooleanField(null=False, blank=False, default=False)
    email = models.EmailField(max_length=150, blank=True)
    cpf = models.DecimalField(null=True, unique=True, max_digits=11, decimal_places=0, blank=True, verbose_name=_("CPF"))
    telefone = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    telefone_comercial = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    expiracao_acesso_wifi = models.DateTimeField(null=True, blank=True, verbose_name=_(u"Data de expiração do Acesso Wi-Fi"))
    senha = models.CharField(max_length=25, blank=True)

    data_cadastro = models.DateTimeField(null=True, auto_now_add=True, blank=True)
    data_ultima_alteracao = models.DateTimeField(null=True, auto_now=True, blank=True)

    image_path = models.ImageField(upload_to="visitantes", blank=True)

    group_name = 'visitantes'
    radius_database = 'radius'

    deleted = False

    def cpf_display(self):
        if self.cpf is None:
            return ''
        str = "%011d" % (self.cpf)
        return "%s.%s.%s-%s" % (str[:3], str[3:6], str[6:9], str[9:])

    def identidade_display(self):
        if self.passaporte:
            return self.identidade
        return "%s-%s/%s" % (self.identidade, self.emissor, self.uf)

    def cpf_username(self, rawcpf=None):
        if rawcpf is None:
            return "%011d" % (self.cpf)
        else:
            return "%011d" % (rawcpf)

    def __telefone_display(self, telefone):
        tel_str = str(telefone)
        if len(tel_str) == 11:
            return "(%s) %s-%s" % (tel_str[:2], tel_str[2:7], tel_str[7:])
        else:
            return "(%s) %s-%s" % (tel_str[:2], tel_str[2:6], tel_str[6:])

    def telefone_display(self):
        return self.__telefone_display(self.telefone)

    def telefone_comercial_display(self):
        return self.__telefone_display(self.telefone_comercial)

    def generate_password(self):
        self.senha = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))

    def update_attributes(self):
        self.delete_all_attributes()
        self.insert_all_attributes()

    def insert_all_attributes(self):
        self.__insert_group()
        self.__insert_check()

    def delete_all_attributes(self, username=None):
        if username is None and self.cpf is not None:
            username = self.cpf_username()

        if username is None:
            return

        self.__delete_group(username)
        self.__delete_check(username)

    def __delete_check(self, delusername):
        objects = radius.Radcheck.objects.using(self.radius_database).filter(username=delusername)
        for obj in objects:
            obj.delete()

    def __delete_group(self, delusername):
        objects = radius.Radusergroup.objects.using(self.radius_database).filter(username=delusername)
        for obj in objects:
            obj.delete()

    def __wifi_enabled(self):
        # Só insere os atributos se tiver o wifi configurado e a expiração não tiver vencido.
        if not self.wifi:
            return False
        if self.expiracao_acesso_wifi is None:
            return False
        if self.expiracao_acesso_wifi >= timezone.now():
            return True
        return False

    # Vincula ao grupo de visitantes
    def __insert_group(self):
        if not self.__wifi_enabled():
            return

        user_group = radius.Radusergroup()
        user_group.groupname = self.group_name
        user_group.username = self.cpf_username()
        user_group.priority = 1
        user_group.save(using=self.radius_database)

    # Insere os atribustos de checagem do Radius para essa máquina
    def __insert_check(self):
        if not self.__wifi_enabled():
            return

        # Atributo para fazer o MAC Authentication
        pass_attribute = radius.Radcheck()
        pass_attribute.username = self.cpf_username()
        pass_attribute.value = self.senha
        pass_attribute.op = ":="
        pass_attribute.attribute = "Cleartext-Password"

        expiry_attribute = radius.Radcheck()
        expiry_attribute.username = self.cpf_username()
        # Gera a string de data e hora no formato reconhecido pelo rlm_expiration do Freeradius
        expiry_attribute.value = self.expiracao_acesso_wifi.strftime('%B %d %Y %H:%M:%S')
        expiry_attribute.op = ":="
        expiry_attribute.attribute = "Expiration"

        # Salva os atributos
        expiry_attribute.save(using=self.radius_database)
        pass_attribute.save(using=self.radius_database)

    def save(self, *args, **kwargs):
        self.emissor = self.emissor.upper()

        if not self.deleted:
            self.update_attributes()

        # Se não tiver senha tem que gerar
        if self.senha is None or self.senha == '':
            self.generate_password()
        super(Visitante, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted = True

        if self.image_path is not None:
            try:
                if path.exists(self.image_path.path):
                    self.image_path.delete()
            except:
                pass

        self.delete_all_attributes()

        super(Visitante, self).delete(*args, **kwargs)

    def __unicode__(self):
        return "%s - %s - ID:%s" % (self.nome, self.identidade_display(), self.id)

    class Meta:
        unique_together = (("identidade", "emissor", "uf", "passaporte"),)
        db_table = 'visitante'

class Registros(models.Model):
    id = util.BigAutoField(primary_key=True)
    dataehora = models.DateTimeField(null=True, blank=False, verbose_name="Data e hora")
    entrada = models.BooleanField(null=False, blank=False, default=False)
    observacao = models.CharField(max_length=300, blank=True, verbose_name="Observação")
    visitante = models.ForeignKey(Visitante, db_column='fk_visitante')
    funcionario_contato = models.DecimalField(null=True, max_digits=15, decimal_places=0, blank=True, verbose_name="Funcionário contato")
    setor_contato = models.CharField(max_length=45, blank=True, verbose_name="Setor contato")
    usuario = models.ForeignKey(User, null=True, db_column='fk_usuario', blank=False, verbose_name="Usuário")

    def funcionario_ldap(self):
        if self.funcionario_contato is None:
            return None

        try:
            funcionario = LdapUser.objects.get(employeenumber=self.funcionario_contato)
        except:
            return None

        return funcionario

    def save(self, *args, **kwargs):
        if self.entrada:
            # Altera a expiração do acesso com base na data e hora de entrada
            nova_expiracao = datetime.datetime(self.dataehora.year, self.dataehora.month, self.dataehora.day, 22, 30, 0)
            #nova_expiracao = timezone.get_default_timezone().localize(nova_expiracao)
	    

            # Só altera se for maior do que já está cadastrado
            if self.visitante.expiracao_acesso_wifi is None or \
               nova_expiracao > self.visitante.expiracao_acesso_wifi:
                self.visitante.expiracao_acesso_wifi = nova_expiracao
            # Salva alteração no visitante
            self.visitante.save()

        super(Registros, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s - %s - %s" % (self.visitante, self.dataehora, self.entrada)

    class Meta:
        db_table = 'registros'

class Log(models.Model):
    created = models.DateTimeField(_(u'Data'), auto_now_add=True, db_index=True)
    user = models.ForeignKey('auth.User')
    msg = models.TextField()

    class Meta:
        verbose_name = _(u'Log')
        verbose_name_plural = (_(u'Logs'))
        db_table = 'weblog'

    def __unicode__(self):
        return self.msg
