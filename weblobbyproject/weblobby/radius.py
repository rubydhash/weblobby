__author__ = 'jimmy'

from django.db import models

class Radcheck(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    def __unicode__(self):
        return "%s[%s] %s %s" % (self.username, self.attribute, self.op, self.value)

    class Meta:
        db_table = 'radcheck'

class Radgroupcheck(models.Model):
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    def __unicode__(self):
        return "%s[%s] %s %s" % (self.username, self.attribute, self.op, self.value)

    class Meta:
        db_table = 'radgroupcheck'

class Radgroupreply(models.Model):
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    def __unicode__(self):
        return "%s[%s] %s %s" % (self.username, self.attribute, self.op, self.value)

    class Meta:
        db_table = 'radgroupreply'

class Radreply(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    def __unicode__(self):
        return "%s[%s] %s %s" % (self.username, self.attribute, self.op, self.value)

    class Meta:
        db_table = 'radreply'

class Radusergroup(models.Model):
    username = models.CharField(primary_key=True, max_length=64)
    groupname = models.CharField(max_length=64)
    priority = models.IntegerField()

    def __unicode__(self):
        return "%s %s %s" % (self.username, self.groupname, self.priority)

    class Meta:
        db_table = 'radusergroup'