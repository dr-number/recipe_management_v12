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
            'view_customdocument',
            'add_customdocument',
            'change_customdocument',
            'view_user'
        ]
    )
    admin_group, created = Group.objects.get_or_create(name='get_or_create_admin_shef')
    admin_group.permissions.set(permissions)
    return admin_group

