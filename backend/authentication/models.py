from django.conf import settings
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField, JSONField

from backend.storage_backends import PrivateMediaStorage

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. \
            Up to 15 digits allowed."
)


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def create_user(self, username, email, password=None, first_name=None, last_name=None):
        """Create and return a `User` with an email, username and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=self.normalize_email(email), email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    role = models.CharField(max_length=20, choices=(['Candidate', 'Candidate'], ['Interviewer', 'Interviewer']), null=True, blank=True)
    profile_picture = models.FileField(upload_to=settings.PROFILE_PICTURE, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return "{first_name} {last_name}".format(first_name=self.first_name, last_name=self.last_name)

    def get_short_name(self):
        return self.first_name


class Skill(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super(Skill, self).save(*args, **kwargs)


class CandidateProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professional_status = models.CharField(max_length=54, choices=settings.PROFESSIONAL_STATUS_CHOICES)
    education = models.CharField(max_length=128, null=True, blank=True)
    college = models.CharField(max_length=128, null=True, blank=True)
    year_of_passing = models.CharField(max_length=54, null=True, blank=True)
    resume = models.FileField(upload_to=settings.RESUME_STORE, null=False, blank=False, storage=PrivateMediaStorage())
    linkedin = models.URLField(max_length=256, null=True, blank=True)
    industry = models.CharField(max_length=256, null=True, blank=True)
    designation = models.CharField(max_length=256, null=True, blank=True)
    company = models.CharField(max_length=256, null=True, blank=True)
    exp_years = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(0, message='Enter a whole number')])
    skills = models.ManyToManyField(to=Skill)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()


class InterviewerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    industry = models.CharField(max_length=256, null=True, blank=True)
    designation = models.CharField(max_length=256, null=True, blank=True)
    company = models.CharField(max_length=256, null=True, blank=True)
    exp_years = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(0, message='Enter a whole number')])
    resume = models.FileField(upload_to=settings.RESUME_STORE, null=False, blank=False, storage=PrivateMediaStorage())
    linkedin = models.URLField(max_length=256, null=True, blank=True)
    skills = models.ManyToManyField(to=Skill)
    account_info = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()


class Interview(models.Model):
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField()
    exp_years = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(0, message='Enter a whole number')])
    timezone = models.CharField(max_length=256)
    skills = models.ManyToManyField(to=Skill)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title


class InterviewSlots(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    interview_start_time = models.DateTimeField()
    interview_end_time = models.DateTimeField()
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.interview.job_title

