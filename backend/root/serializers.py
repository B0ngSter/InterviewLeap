from rest_framework import serializers
from authentication.models import Skill, Interview, InterviewSlots
from authentication.serializers import SkillSerializer
from .models import BookInterview, PaymentDetails
from django.db import transaction, IntegrityError


class BookInterviewCreateSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    def validate(self, data):
        if not data.get('company_type'):
            raise serializers.ValidationError({"message": "Please select which type of company you want to be interviewed."})
        if not data.get('skills'):
            raise serializers.ValidationError({"message": "Please select your top five skills"})
        if len(data.get('skills')) > 5:
            raise serializers.ValidationError({"message": "Top five skills are allowed"})
        if not data.get('applied_designation'):
            raise serializers.ValidationError({"message": "Please mention your role/title for the interview"})
        if not data.get('date'):
            raise serializers.ValidationError({"message": "Mention a date for the interview"})
        if not data.get('time_slots'):
            raise serializers.ValidationError({"message": "Choose time slots of your convenience"})
        # if not len(data.get('time_slots')) == 3:
        #     raise serializers.ValidationError({"message": "Select 3 suitable time slots for interview"})

        return data

    class Meta:
        model = BookInterview
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                skills = validated_data.pop('skills')
                skill_obj = [Skill.objects.get_or_create(title=skill.get('title'))[0] for skill in skills]
                candidate = BookInterview.objects.create(**validated_data)
                candidate.skills.set(skill_obj)
                candidate.save()
                return candidate
        except IntegrityError:
            transaction.rollback()


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentDetails
        fields = '__all__'


class SKillSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['title']


class FeedbackCreateViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterviewSlots
        fields = ['feedback']

