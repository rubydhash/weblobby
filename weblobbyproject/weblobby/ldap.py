__author__ = 'jimmy'

from django.conf import settings

from ldapdb.models.fields import CharField, ImageField, IntegerField, ListField
import ldapdb

class LdapUser(ldapdb.models.Model):
    base_dn = settings.LDAP_USERS_DN
    object_class = ['*']
    uid = CharField(db_column='uid', primary_key=True)
    employeenumber = CharField(db_column='employeeNumber', blank=True)
    displayname = CharField(db_column='displayName', blank=True)

    def __unicode__(self):
        return '%s' % (self.displayname)

    class Meta:
        ordering = 'uid',

class LdapGroup(ldapdb.models.Model):
    base_dn = settings.LDAP_GROUPS_DN
    object_class = ['*']
    cn = CharField(db_column='cn', primary_key=True)

    def __unicode__(self):
        return '%s' % (self.cn)

    class Meta:
        ordering = 'cn',