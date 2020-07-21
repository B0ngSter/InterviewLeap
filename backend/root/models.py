from django.conf import settings
from django.db import models
from authentication.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class BookInterview(models.Model):
    company_type = models.CharField(max_length=30, null=True, blank=True)
    professional_status = models.CharField(max_length=64, choices=settings.PROFESSIONAL_STATUS_CHOICES, null=True, blank=True)
    applied_designation = models.CharField(max_length=120, null=True, blank=True)
    date = models.DateField(help_text='Select date for interview @candidate side')
    time_slots = ArrayField(models.CharField(max_length=150), null=True, blank=True)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)