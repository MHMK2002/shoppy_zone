from django.contrib import admin

from account.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'date_joined']
    fieldsets = (
        (
            'General',
            {
                'fields': ['username', 'first_name', 'last_name', 'email']
            }
        ),
        (
            'Permission',
            {
                'classes': ['collapse'],
                'fields': ['is_superuser', 'is_staff', 'user_permissions', 'groups']
            }
        ),
        (
            'Activity',
            {
                'classes': ['collapse'],
                'fields': ['last_login', 'date_joined', 'is_active']
            }
        )
    )
