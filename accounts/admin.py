from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('个人信息', {'fields': ('phone',)}),
        ('权限', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'phone', 'password1', 'password2'),
        }),
    )
