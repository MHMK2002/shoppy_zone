from django.contrib import admin
from django.db.models import QuerySet

from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['username']
    list_display = ['username', 'name', 'first_name', 'last_name', 'is_active']
    list_editable = ['first_name', 'last_name', 'is_active']
    list_display_links = ['username']
    readonly_fields = ['username']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['is_active', 'is_superuser']
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
    actions = ['make_admin', 'make_user_clear']

    @admin.display()
    def name(self, obj: User):
        return f'{obj.first_name} {obj.last_name}' if obj.first_name or obj.last_name else None

    def get_empty_value_display(self):
        return '(none)'

    @admin.action(description='Make admin')
    def make_admin(self, request, queryset):
        queryset.update(is_superuser=True)

    @admin.action(description='Make user clear')
    def make_user_clear(self, request, queryset: QuerySet[User]):
        queryset.update(last_login=None, first_name='', last_name='')

