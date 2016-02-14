from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_migrate

from .connectors import add_view_only_permission

class TimeAuditModel(models.Model):
    ''' To track when the record was created and last modified'''
    created_at = models.DateTimeField('Created At',
        auto_now_add=True)
    updated_at = models.DateTimeField('Updated At',
        auto_now=True)

    class Meta:
        abstract = True


class UserAuditModel(models.Model):
    '''To track who created and last modified the record'''
    created_by = models.ForeignKey(User, related_name='created_%(class)s_set',
                                   null=True, blank=True, verbose_name='Created By')
    updated_by = models.ForeignKey(User, related_name='updated_%(class)s_set',
                                  null=True, blank=True, verbose_name='Updated By')

    class Meta:
        abstract = True


class AuditModel(TimeAuditModel, UserAuditModel):
    '''To track by who and when was the last record modified'''

    class Meta:
        abstract = True


class Book(models.Model):
    name = models.CharField(max_length=255)
    isbn = models.CharField(max_length=12)

    class Meta:
        db_table = 'books'


post_migrate.connect(add_view_only_permission)
