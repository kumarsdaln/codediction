from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def group_required(*group_names):
    """
    Decorator to restrict access to users based on their group membership.

    Usage:
    @group_required('Admin', 'Teacher', 'Student')
    def some_view(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.groups.filter(name__in=group_names).exists() or request.user.is_staff:
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                return redirect('login')
        return _wrapped_view
    return decorator
