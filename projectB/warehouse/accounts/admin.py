from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'department', 'is_active')
    list_filter = ('user_type', 'is_active', 'is_staff', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'department')}),
        (_('Permissions'), {
            'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'department'),
        }),
    )

    actions = ['make_warehouse_manager', 'make_warehouse_staff']

    @admin.action(description='Convertir a Warehouse Manager')
    def make_warehouse_manager(self, request, queryset):
        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name='warehouse_manager')
        for user in queryset:
            user.user_type = 'warehouse'
            user.save()
            user.groups.add(group)
        self.message_user(request, f"{queryset.count()} usuarios convertidos a Warehouse Manager")

    @admin.action(description='Convertir a Warehouse Staff')
    def make_warehouse_staff(self, request, queryset):
        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name='warehouse_staff')
        for user in queryset:
            user.user_type = 'warehouse'
            user.save()
            user.groups.add(group)
        self.message_user(request, f"{queryset.count()} usuarios convertidos a Warehouse Staff")