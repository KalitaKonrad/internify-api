from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'username')
    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'id', 'username',
                    'is_active', 'is_verified', 'is_staff', 'is_company', 'is_employee')

    fieldsets = (
        ('General information', {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('description',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_verified', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)
