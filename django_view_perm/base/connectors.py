from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def add_view_only_permission(sender, **kwargs):
    '''This creates a view only permission for sender'''
    for content_type in ContentType.objects.all():
        codename = 'can_view_%s_only'%content_type.model
        name = 'Can View %s only' % content_type.name
        if not Permission.objects.filter(content_type=content_type,
        codename=codename):
            Permission.objects.create(
            content_type=content_type,
            codename=codename,
            name=name)


