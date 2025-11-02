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

