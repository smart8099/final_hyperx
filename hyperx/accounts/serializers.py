from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import User
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
class RegistrationSerializer(serializers.ModelSerializer):
    USER_TYPE_CHOICES = [
        'MANAGER', 'REGISTRAR', 'HOSPITAL_SUPERVISOR',
        'NURSE', 'LAB_TECHNICIAN', 'PHYSICIAN', 'PHARMACIST'
    ]

    DEFAULT_PASSWORD_FOR_NEWLY_REGISTERED_USERS = getattr(settings,"DEFAULT_PASSWORD_FOR_NEWLY_REGISTERED_USERS",'')
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'user_type']

    def validate_phone_number(self, phone_number):
        if not phone_number.isdigit():
            raise serializers.ValidationError("Phone number should contain only digits")

        if not phone_number.startswith('0'):
            raise serializers.ValidationError("Phone number should start with '0'")

        if len(phone_number) < 10 or len(phone_number) > 10:
            raise serializers.ValidationError("Phone number should be exactly 10 digits")

        return phone_number

    def validate_username(self, username):
        if not username.isalnum():
            raise serializers.ValidationError("The username should only contain alphanumeric characters")
        return username

    def validate_email(self, email):
        try:
             validate_email(email)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")

        return email



    def validate_user_type(self, user_type):
        if user_type not in self.USER_TYPE_CHOICES:
            raise serializers.ValidationError("Invalid user type")
        return user_type

    def validate(self, attrs):
        required_fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'user_type']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError(f"{field.replace('_', ' ').capitalize()} is required")

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(self.DEFAULT_PASSWORD_FOR_NEWLY_REGISTERED_USERS)
        user.save()

        return user
