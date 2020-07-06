from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core import exceptions
from .models import User
from django.conf import settings


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
