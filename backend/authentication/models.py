from django.conf import settings
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

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

    def create_user(self, email, password=None, first_name=None, last_name=None, role=None):
        """Create and return a `User` with an email, username and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=email, email=self.normalize_email(email), first_name=first_name, last_name=last_name, role=role)
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
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
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
    role = models.CharField(max_length=20, choices=(['candidate', 'candidate'], ['interviewer', 'interviewer']))
    profile_picture = models.FileField(upload_to=settings.PROFILE_PICTURE, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']
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
    education = models.CharField(max_length=128, null=True, blank=True)
    college = models.CharField(max_length=128, null=True, blank=True)
    year_of_passing = models.CharField(max_length=54, null=True, blank=True)
    job_title = models.CharField(max_length=256)
    resume = models.FileField(upload_to=settings.RESUME_STORE)
    linkedin = models.URLField(max_length=256, null=True, blank=True)
    skills = models.ManyToManyField(to=Skill)


class InterviewerProfile(models.Model):
    industry = models.CharField(max_length=256, null=True, blank=True)
    designation = models.CharField(max_length=256, null=True, blank=True)
    company = models.CharField(max_length=256, null=True, blank=True)
    exp_years = models.IntegerField(null=True, blank=True, validators=[
        MinValueValidator(0, message='Enter a whole number')])
    resume = models.FileField(upload_to=settings.RESUME_STORE)
    linkedin = models.URLField(max_length=256, null=True, blank=True)
    skills = models.ManyToManyField(to=Skill)


