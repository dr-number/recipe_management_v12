from rest_framework.permissions import BasePermission

from main.models import User
from main.const import KEY_USER_TYPE_CHEF

class IsChefUser(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user
        if not user:
            return False

        return user.is_authenticated and user.type == KEY_USER_TYPE_CHEF
