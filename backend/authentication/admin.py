from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    UserAdmin.fieldsets += ('Custom fields set', {'fields': ('email_verified', 'role', 'profile_picture')}),

    model = User
    readonly_fields = ['date_joined']


class CompanyProfileAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super(CompanyProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-created_at')
        return queryset


admin.site.register(User, CustomUserAdmin)