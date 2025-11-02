from django.contrib import admin
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission, Group

from main.models import User
from main.const import KEY_USER_TYPE_CHEF

class IsChefUser(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user
        if not user:
            return False

        return user.is_authenticated and user.type == KEY_USER_TYPE_CHEF

def get_or_create_admin_shef():
    permissions = Permission.objects.filter(
        codename__in=[
            'view_recipecategory',
            'view_comment', 'add_comment', 'change_comment', 'delete_comment',
            'view_recipe', 'add_recipe', 'change_recipe', 'delete_recipe',
        ]
    )
    admin_group, created = Group.objects.get_or_create(name='admin_shef')
    admin_group.permissions.set(permissions)
    return admin_group

class ChefUserRestrictedAdmin(admin.ModelAdmin):
    user_field = 'user'  # имя поля с пользователем
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(**{self.user_field: request.user})

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            readonly_fields = list(readonly_fields) + [self.user_field]
        return list(set(readonly_fields))

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
            return

        if not change:
            setattr(obj, self.user_field, request.user)
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return getattr(obj, self.user_field) == request.user
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return getattr(obj, self.user_field) == request.user
        return super().has_delete_permission(request, obj)
