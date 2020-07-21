from rest_framework import serializers
from .models import BookInterview


class BookInterviewCreateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if not data.get('company_type'):
            raise serializers.ValidationError({"message": "Please select which type of company you want to be interviewed."})
        if not data.get('professional_status'):
            raise serializers.ValidationError({"message": "Please select the You'r a(professional status)"})
        if not data.get('applied_designation'):
            raise serializers.ValidationError({"message": "Please mention your role/title for the interview"})
        if not data.get('date'):
            raise serializers.ValidationError({"message": "Mention a date for the interview"})
        if not data.get('time_slots'):
            raise serializers.ValidationError({"message": "Choose time slots of your convenience"})

        return data

    class Meta:
        model = BookInterview
        fields = '__all__'
