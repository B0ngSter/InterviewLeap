from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    UserAdmin.fieldsets += ('Custom fields set', {'fields': ('role',)}),

    model = User
    readonly_fields = ['date_joined']


admin.site.register(User, CustomUserAdmin)