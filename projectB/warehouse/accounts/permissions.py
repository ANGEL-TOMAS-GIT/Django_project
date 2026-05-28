from rest_framework.permissions import BasePermission


class HasGroupPermission(BasePermission):
    def has_permission(self, request, view):
        required_group = getattr(view, 'required_group', None)
        if not required_group:
            return True

        if not request.user.is_authenticated:
            return False

        user_groups = request.user.groups.values_list('name', flat=True)
        return any(group in user_groups for group in required_group)
