from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import User
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from django.contrib.auth.models import Group
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

class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.

    Validates the provided username or email and password,
    and authenticates the user.

    Attributes:
        username_or_email (str): The username or email for authentication.
        password (str): The password for authentication.
        username (str): The username of the authenticated user.
        tokens (str): The authentication tokens.

    Raises:
        AuthenticationFailed: If the provided credentials are invalid or the user is not active

    Returns:
        dict: The serialized user data and tokens.

    """

    staff_id_or_email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)
    DEFAULT_PASSWORD_FOR_NEWLY_REGISTERED_USERS = getattr(settings,"DEFAULT_PASSWORD_FOR_NEWLY_REGISTERED_USERS",'')
    class Meta:
        model = User
        fields = ["staff_id_or_email", "password", "username", "tokens"]

    def user_token(self, user):
        refresh = RefreshToken.for_user(user)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def user_role(self, user):
        group = user.groups.all().first()
        role_name = group.name

        return role_name

    def validate(self, attrs):
        staff_id_or_email = attrs.get("staff_id_or_email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(username=staff_id_or_email, password=password)

        change_default_password = False

        if password == self.DEFAULT_PASSWORD_FOR_NEWLY_REGISTERED_USERS:
            change_default_password = True

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")

        return {
            "staff_id": user.username,
            "user_role": self.user_role(user),
            "change_default_password" : change_default_password,
            "tokens": self.user_token(user),
        }
