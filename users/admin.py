"""User admin classes"""

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Register your models here.

#Models
from django.contrib.auth.models import User
from users.models import Profile

# Register Profile
# admin.site.register(Profile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = ('pk', 'user', 'phone_number', 'website', 'picture')
    list_display_links = ('pk', 'user')
    list_editable = ('phone_number', 'website', 'picture')
    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
        'phone_number'
    )

    list_filter = ('created', 'modified', 'user__is_active','user__is_staff')

    fieldsets = (
        ('Profile', {
            'fields': (
                ('user', 'picture'),
            ),
        }),
        ('Extra Info', {
            'fields':(
                ('phone_number', 'website'),
                ('biography'),
            )
        }),
        ('Metadata', {
            'fields': (('created', 'modified'),
            ),
        }),
    )

    readonly_fields = ('created', 'modified')

"""
Une los modelos de usuario y perfil para no tener que crear un usuario para asociarlo con un perfil
"""
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)
    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

