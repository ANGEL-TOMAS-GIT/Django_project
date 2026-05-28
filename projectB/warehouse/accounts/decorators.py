# accounts/decorators.py
from django.core.exceptions import PermissionDenied
from functools import wraps


def permission_required(perm):
    """Decorator to check user permissions"""
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(perm):
                raise PermissionDenied(f"You don't have permission: {perm}")
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    return decorator


def group_required(*group_names):
    """Decorator to check if user belongs to any of the required groups"""
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("You must be logged in")
            
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(group in user_groups for group in group_names):
                return view_func(request, *args, **kwargs)
            
            raise PermissionDenied(f"You need one of these groups: {', '.join(group_names)}")
        
        return wrapped_view
    
    return decorator

