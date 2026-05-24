from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("phone_number", "email", "full_name", "is_staff", "is_active")
    ordering = ("email",)

    fieldsets = (
        ("Basic Info", {"fields": ("email", "password")}),
        (_("Personal Info"),
         {
             "fields": (
                 "first_name",
                 "last_name",
                 "phone_number",
                 "date_of_birth",
                 "pref_lang",
                 "profile_image",
             ),
         },
         ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    @staticmethod
    def full_name(obj):
        return f'{obj.first_name} {obj.last_name}'.strip()
