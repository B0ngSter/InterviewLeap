from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core import exceptions
from .models import User, Interview
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


# class SkillReadSerializer(serializers.ModelSerializer):
#     title = serializers.SerializerMethodField()
#
#     def get_title(self, obj):
#         return obj.title
#
#     class Meta:
#         model = Skill
#         fields = ['title']


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['title']


class CandidateProfileCreateListSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = CandidateProfile
        fields = ['user', 'education', 'college', 'year_of_passing', 'job_title', 'resume', 'linkedin', 'skills']

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        candidate, created = CandidateProfile.objects.get_or_create(user=self.context['request'].user)
        candidate.skills.set(skill_obj)
        candidate.__dict__.update(**validated_data)
        candidate.save()
        return candidate


class InterviewerProfileCreateListSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = InterviewerProfile
        fields = ['user', 'industry', 'designation', 'company', 'exp_years', 'resume', 'linkedin', 'skills']

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

    class Meta:
        model = Interview
        fields = ['interviewer', 'job_title', 'exp_years', 'date', 'time_slots']

