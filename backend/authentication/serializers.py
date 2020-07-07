from rest_framework import serializers
from authentication.models import CandidateProfile, InterviewerProfile, Skill


class CandidateSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['title']


class CandidateProfileCreateListSerializer(serializers.ModelSerializer):
    skills = CandidateSkillSerializer(many=True)

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


class CandidateProfileDetailtSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        fields = ['education', 'college', 'year_of_passing', 'job_title', 'resume', 'linkedin', 'skills']


class InterviewerProfileDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterviewerProfile
        fields = ['industry', 'designation', 'company', 'exp_years', 'resume', 'linkedin', 'skills']
