from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core import exceptions
from .models import User
from django.conf import settings
from authentication.models import CandidateProfile, InterviewerProfile, Skill


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(read_only=True)
    role = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'token', 'role', 're_password']

    def validate(self, data):
        user = None
        password = data.get('password')
        re_password = data.get('re_password')

        errors = dict()

        if password != re_password:
            errors['message'] = 'Password and confirm password does not match, please type again'
        try:
            validate_password(password=password,
                              user=user,
                              password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
        except exceptions.ValidationError as e:
            errors['message'] = " ,".join(e.messages)

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
        fields = ['education', 'college', 'year_of_passing', 'job_title', 'resume', 'linkedin', 'skills']

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        candidate = CandidateProfile.objects.create(**validated_data)
        candidate.skills.set(skill_obj)
        candidate.save()
        return candidate


class InterviewerProfileCreateListSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = InterviewerProfile
        fields = ['industry', 'designation', 'company', 'exp_years', 'resume', 'linkedin', 'skills']

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        interviewer = InterviewerProfile.objects.create(**validated_data)
        interviewer.skills.set(skill_obj)
        interviewer.save()
        return interviewer


class CandidateProfileDetailSerializer(serializers.ModelSerializer):

    skills = SkillSerializer(many=True)

    class Meta:
        model = CandidateProfile
        fields = ['education', 'college', 'year_of_passing', 'job_title', 'resume', 'linkedin', 'skills']

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
        fields = ['industry', 'designation', 'company', 'exp_years', 'resume', 'linkedin', 'skills']

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills')
        skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
        instance.skills.set(skill_obj)
        instance.save()
        return instance
