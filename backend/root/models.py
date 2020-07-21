from django.conf import settings
from django.db import models
from authentication.models import User, Skill
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class BookInterview(models.Model):
    company_type = models.CharField(max_length=30, null=True, blank=True)
    applied_designation = models.CharField(max_length=120, null=True, blank=True,
                                           help_text='role(profile) of the candidate they want to be interviewed for e.g java developer')
    date = models.DateField(help_text='Select date for interview @candidate side', null=True, blank=True)
    time_slots = ArrayField(models.CharField(max_length=150), null=True, blank=True)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(to=Skill)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)