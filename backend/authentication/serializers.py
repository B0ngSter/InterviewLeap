import datetime

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core import exceptions

from root.models import BookInterview
from .models import User, Interview, InterviewSlots
from django.conf import settings
from authentication.models import CandidateProfile, InterviewerProfile, Skill


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(read_only=True)
    role = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'token', 'role', 'confirm_password']

    def validate(self, data):
        user = None
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        errors = dict()

        email = data.get('email')
        existing_user = User.objects.filter(email=email).exists()
        if existing_user:
            errors['message'] = "user with this email already exists."
        if not data.get('first_name'):
            errors['message'] = "Please enter your first name"
        if not data.get('last_name'):
            errors['message'] = "Please enter your last name"
        if not data.get('email'):
            errors['message'] = "Please enter your email id"
        if not password:
            errors['message'] = "Please enter password for signup"
        if not confirm_password:
            errors['message'] = "Please enter confirm password"
        if password != confirm_password:
            errors['message'] = 'Password and confirm password does not match, please type again'
        try:
            validate_password(password=password,
                              user=user,
                              password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
        except exceptions.ValidationError as e:
            errors['message'] = ", ".join(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super(RegistrationSerializer, self).validate(data)

    def create(self, validated_data):
        user = User(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class ResendVerificationTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email_verified']

    def update(self, instance, validated_data):
        instance.email_verified = True
        instance.save()
        return instance


# class SkillReadSerializer(serializers.ModelSerializer):
#     title = serializers.SerializerMethodField()
#
#     def get_title(self, obj):
#         return obj.title
#
#     class Meta:
#         model = Skill
#         fields = ['title']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile_number']

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'mobile_number']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['title']


class CandidateProfileCreateListSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = CandidateProfile
        fields = ['user', 'professional_status', 'education', 'college', 'year_of_passing', 'resume',
                  'linkedin', 'industry', 'designation', 'company', 'exp_years', 'skills', 'job_title']

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        candidate, created = CandidateProfile.objects.get_or_create(user=self.context['request'].user)
        candidate.skills.set(skill_obj)
        candidate.__dict__.update(**validated_data)
        candidate.save()
        return candidate


class CandidateFresherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = ['user', 'professional_status', 'education', 'college', 'year_of_passing', 'resume',
                  'linkedin', 'industry', 'designation', 'skills', 'job_title', 'company', 'exp_years']


class CandidateExperienceSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = CandidateProfile
        fields = ['user', 'professional_status', 'education', 'college', 'year_of_passing', 'resume',
                  'linkedin', 'industry', 'designation', 'skills', 'job_title']


class InterviewerProfileCreateListSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = InterviewerProfile
        fields = ['user', 'industry', 'designation', 'company', 'exp_years', 'linkedin', 'skills',
                  'account_info', 'resume']

    def validate(self, data):
        account_info = data['account_info']
        message = "{} field is required"
        if 'acc_name' not in account_info:
            raise serializers.ValidationError({"message": message.format('Account Name')})
        if 'account_number' not in account_info:
            raise serializers.ValidationError({"message": message.format('Account Number')})
        if 'ifsc_code' not in account_info:
            raise serializers.ValidationError({"message": message.format('IFSC Code')})
        if 'bank' not in account_info:
            raise serializers.ValidationError({"message": message.format('Bank')})
        return data

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        interviewer, created = InterviewerProfile.objects.get_or_create(user=self.context['request'].user)
        interviewer.skills.set(skill_obj)
        interviewer.__dict__.update(**validated_data)
        interviewer.save()
        return interviewer


class CandidateProfileDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = CandidateProfile
        fields = ['user', 'education', 'college', 'year_of_passing', 'job_title', 'resume', 'linkedin', 'skills']

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        instance.skills.set(skill_obj)
        instance.save()
        return instance


class InterviewerProfileDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = InterviewerProfile
        fields = ['user', 'industry', 'designation', 'company', 'exp_years', 'resume', 'linkedin', 'skills',
                  'account_info']

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        instance.skills.set(skill_obj)
        instance.save()
        return instance


class InterviewCreateSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Interview
        fields = ['slug', 'interviewer', 'job_title', 'description', 'exp_years', 'timezone', 'quoted_price', 'skills']

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        if validated_data.get('slug', None):
            interview_obj = Interview.objects.get(interviewer=self.context['request'].user,
                                                  slug=validated_data['slug'])
        else:
            interview_obj = Interview.objects.create(interviewer=self.context['request'].user)
        interview_obj.skills.set(skill_obj)
        interview_obj.__dict__.update(**validated_data)
        interview_obj.save()
        time_slots = self.context['request'].data['interview_time']
        date_time_list = []
        for date, time_lists in time_slots.items():
            for time in time_lists:
                start_time = time.split("-")[0].strip()
                end_time = time.split("-")[1].strip()
                start_date_time = self._date_time_naive_format(date, start_time)
                end_date_time = self._date_time_naive_format(date, end_time)
                date_time_list.append((start_date_time, end_date_time))
        timeslot_lists = [InterviewSlots(interview=interview_obj, interview_start_time=start_date_time,
                                         interview_end_time=end_date_time)
                          for start_date_time, end_date_time in date_time_list]
        InterviewSlots.objects.bulk_create(timeslot_lists)
        return interview_obj

    def _date_time_naive_format(self, date, time):
        date_time = date + ' ' + time
        naive = datetime.datetime.strptime(date_time, "%m-%d-%Y %H:%M")
        return naive


class InterviewerRequestsListSerializer(serializers.ModelSerializer):
    is_feedback = serializers.SerializerMethodField()
    candidate_email = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    def get_is_feedback(self, obj):
        if obj.feedback:
            return True
        return False

    def get_candidate_email(self, obj):
        return obj.candidate.email

    def get_resume(self, obj):
        resume = CandidateProfile.objects.get(user__email=obj.candidate.email).resume.url
        return resume

    class Meta:
        model = BookInterview
        fields = ['slug', 'applied_designation', 'date', 'time_slots', 'candidate_email', 'is_feedback', 'resume']


class CustomInterviewSerializer(serializers.ModelSerializer):
    candidate_email = serializers.SerializerMethodField()
    mock_interview = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    def get_candidate_email(self, obj):
        return obj.candidate.email

    def get_resume(self, obj):
        resume = CandidateProfile.objects.get(user__email=obj.candidate.email).resume.url
        return resume

    def get_mock_interview(self, obj):
        return True

    class Meta:
        model = BookInterview
        fields = ['slug', 'applied_designation', 'date', 'interview_start_time', 'interview_end_time',
                  'candidate_email', 'mock_interview', 'meet_link', 'resume']


class MockInterviewSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    applied_designation = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    interview_start_time = serializers.SerializerMethodField()
    interview_end_time = serializers.SerializerMethodField()
    candidate_email = serializers.SerializerMethodField()
    custom_interview = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    def get_slug(self, obj):
        return obj.interview.slug

    def get_applied_designation(self, obj):
        return obj.interview.job_title

    def get_date(self, obj):
        return obj.interview_start_time.date()

    def get_interview_start_time(self, obj):
        return obj.interview_start_time.time()

    def get_interview_end_time(self, obj):
        return obj.interview_end_time.time()

    def get_candidate_email(self, obj):
        if obj.candidate:
            return obj.candidate.user.email

    def get_resume(self, obj):
        if obj.candidate:
            return obj.candidate.resume.url

    def get_custom_interview(self, obj):
        return True

    class Meta:
        model = InterviewSlots
        fields = ['slug', 'applied_designation', 'date', 'interview_start_time', 'interview_end_time',
                  'candidate_email', 'custom_interview', 'resume']


class PastInterviewSerializer(serializers.ModelSerializer):
    candidate_email = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    def get_candidate_email(self, obj):
        if obj.candidate:
            return obj.candidate.user.email

    def get_resume(self, obj):
        if obj.candidate:
            return obj.candidate.resume.url

    def get_role(self, obj):
        return obj.interview.job_title

    class Meta:
        model = InterviewSlots
        fields = ['interview_start_time', 'interview_end_time', 'candidate_email', 'role', 'resume', 'feedback']
