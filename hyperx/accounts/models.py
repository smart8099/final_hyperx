from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, user_type, password=None):
        """
        Create and save a regular user with the given details.
        """
        if not first_name:
            raise ValueError("User should have a first name")

        if not last_name:
            raise ValueError("User should have a last name")

        if not username:
            raise ValueError("The username field is required.")

        if not email:
            raise ValueError("User should have an email")

        if not user_type:
            raise ValueError("User should have a user type")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            user_type=user_type
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)

        # Assign user to appropriate group based on user_type
        group_name = user_type.lower()  # Create group name from user_type
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return user

    def create_superuser(self, username, first_name, last_name, email, user_type, password=None):
        if password is None:
            raise ValueError("Password cannot be None")

        if user_type not in ["Manager", "Registrar", "Clinic Supervisor"]:
            raise ValueError("Invalid user type for creating a superuser")

        user = self.create_user(username,first_name, last_name,  email, user_type, password)
        user = self.create_user(username, first_name, last_name, email, user_type,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('MANAGER', 'MANAGER'),
        ('HOSPITAL_SUPERVISOR', 'HOSPITAL_SUPERVISOR'),
        ('REGISTRAR', 'REGISTRAR'),
        ('NURSE', 'NURSE'),
        ('LAB_TECHNICIAN', 'LAB_TECHNICIAN'),
        ('PHARMACIST', 'PHARMACIST'),
        ('PHYSICIAN', 'PHYSICIAN'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255,db_index=True,unique=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'user_type']

    objects = UserManager()

    def __str__(self) -> str:
        return f'self.email (self.username)'

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }



