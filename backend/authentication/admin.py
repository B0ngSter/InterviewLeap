from .models import User, CandidateProfile, InterviewerProfile, Skill, Interview, InterviewSlots
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    UserAdmin.fieldsets += ('Custom fields set', {'fields': ('role', 'email_verified', 'profile_picture',
                                                             'mobile_number')}),

    model = User
    readonly_fields = ['date_joined']


admin.site.register(User, CustomUserAdmin)
admin.site.register(CandidateProfile)
admin.site.register(InterviewerProfile)
admin.site.register(Skill)
admin.site.register(Interview)
admin.site.register(InterviewSlots)
