from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def system_admin_required(view_func):
    """系统管理员权限装饰器"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_system_admin:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden('您没有系统管理员权限')
    return wrapper

def admin_required(view_func):
    """普通管理员或系统管理员权限装饰器"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_system_admin or request.user.is_admin:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden('您没有管理员权限')
    return wrapper 