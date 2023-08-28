from django.contrib.auth import get_user_model


class EmailBackend(object):
    """
    Custom authentication backend for email-based authentication.

    Allows users to authenticate using their email and password.

    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on email and password.

        Args:
            request (HttpRequest): The HTTP request object.
            username (str): The email used for authentication.
            password (str): The password used for authentication.

        Returns:
            User: The authenticated user instance if the credentials are valid.
            None: If the provided email does not exist or the password is incorrect.

        """
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, "is_active", False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        """
        Retrieve a user instance by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The user instance if found, or None if not found.

        """
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
