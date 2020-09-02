from backend import settings
from django.db import models
from authentication.models import User, Skill, InterviewerProfile
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils.text import slugify
import random
import string


class PaymentDetails(models.Model):
    payment_request_id = models.CharField(max_length=150,  null=True, blank=True)
    buyer = models.EmailField(null=True, blank=True)
    buyer_name = models.CharField(max_length=120, null=True, blank=True)
    buyer_phone = models.CharField(max_length=30, null=True, blank=True)
    amount = models.CharField(max_length=54, null=True, blank=True)
    tax_amount = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=120, null=True, blank=True)
    purpose = models.CharField(max_length=220, null=True, blank=True)
    payment_id = models.CharField(max_length=120,  null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    instrument_type = models.CharField(max_length=50, null=True, blank=True)
    billing_instrument = models.CharField(max_length=200, null=True, blank=True)
    payout_id = models.CharField(max_length=120,  null=True, blank=True)
    payout_at = models.DateTimeField(null=True, blank=True)
    other_detail = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_request_id+'--' + str(self.amount)


class BookInterview(models.Model):
    slug = models.SlugField(max_length=240, null=True, blank=True)
    company_type = models.CharField(max_length=30)
    applied_designation = models.CharField(max_length=120, null=True, blank=True,
                                           help_text='role(profile) of the candidate they want to be interviewed for e.g java developer')
    date = models.DateField(help_text='Select date for interview @candidate side')
    time_zone = models.CharField(max_length=120, null=True, blank=True)
    time_slots = ArrayField(models.CharField(max_length=150))
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(to=Skill)
    interview_start_time = models.DateTimeField(null=True, blank=True)
    interview_end_time = models.DateTimeField(null=True, blank=True)
    is_payment_done = models.BooleanField(default=False)
    is_interview_scheduled = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    interviewer = models.ForeignKey(InterviewerProfile, null=True, blank=True, on_delete=models.CASCADE)
    payment_detail = models.ForeignKey(PaymentDetails, null=True, blank=True, on_delete=models.DO_NOTHING)
    meet_link = models.CharField(max_length=368, null=True, blank=True)
    feedback = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # def generate_booking_id(self):
    #     booking_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    #     while BookInterview.objects.filter(booking_id=booking_id).count() > 0:
    #         booking_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    #     return booking_id

    def save(self, *args, **kwargs):
        super(BookInterview, self).save(*args, **kwargs)
        if not self.slug:
            slug_value = "{}".format(''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
            self.slug = slugify(slug_value)
            self.save()

    def __str__(self):
        return self.slug


class PaymentStatusLog(models.Model):
    payment_request_id = models.CharField(max_length=150)
    status = models.CharField(max_length=120, null=True, blank=True)
    amount = models.CharField(max_length=120)
    tax_amount = models.CharField(max_length=50)
    email = models.EmailField(max_length=40)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    interview_slug = models.CharField(max_length=120)  # This will hold the value against mock/custom booking interview
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_request_id
