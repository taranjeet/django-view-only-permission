from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

class ViewOnlyAdmin(admin.ModelAdmin):
    '''This class makes fields read only'''

    def _is_user_view_only_type(self, perm, request):
        return request.user.has_perm(str(perm)) and request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        class_name = self.__class__.__name__.replace('Admin', '').lower()
        for permission in request.user.get_all_permissions():
            head, sep, tail = permission.partition('.')
            perm = 'can_view_%s_only' % class_name

            if str(perm) == str(tail):
                if self._is_user_view_only_type(perm, request):
                    return flatten_fieldsets(self.declared_fieldsets)
                else:
                    return list(set(
                        [field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]))
        return self.readonly_fields


    def get_list_display(self, request):
        list_display = super(ViewOnlyAdmin, self).get_list_display(request)

        app_label, model_name = self.opts.app_label.lower(), self.model._meta.object_name.lower()

        perm = '%s.can_view_%s_only' % (app_label, model_name)

        if self._is_user_view_only_type(perm, request):
            self.list_editable = ()
        return list_display


    @register.inclusion_tag('admin/submit_line.html', takes_context=True)
    def submit_row(context):
        ctx = original_submit_row(context)
        app_name = context['app_label']
        model_name = context['opts'].model_name

        for permission in context['request'].user.get_all_permissions():
            head, sep, tail = permission.partition('.')
            perm = 'can_view_%s_only' % model_name
            if str(perm) == str(tail):
                if (context['request'].user.has_perm(str(permission)) and
                       not context['request'].user.is_superuser):
                    ctx.update({
                        'show_save_and_add_another' : False,
                        'show_save_and_continue'    : False,
                        'show_save'                 : False,
                        'show_save_as_new'          : False,
                        })
        return ctx
