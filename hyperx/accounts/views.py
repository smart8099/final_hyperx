from drf_yasg.utils import swagger_auto_schema
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView

from hyperx.utils.renderer import CustomAPIResponseRenderer
from rest_framework_simplejwt.tokens import OutstandingToken
from .serializers import RegistrationSerializer,LoginSerializer,PasswordChangeSerializer
from .utilitites import dummy_api_response
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer
    renderer_classes = (CustomAPIResponseRenderer,)

    @swagger_auto_schema(
        operation_summary="Create a new user account",
        operation_description="Accepts data about user and create an account for the user\n"
        "Users have a list roles to choose from, the various roles are as follows:\n"
        "USER_TYPE_CHOICES = [\n"
        "\t'MANAGER'\n"
        "\t'REGISTRAR'\n"
        "\t'HOSPITAL_SUPERVISOR',\n"
        "\t'NURSE',\n"
        "\t'LAB_TECHNICIAN',\n"
        "\t'PHYSICIAN',\n "
        "\t'PHARMACIST'\n"
        "]",
        request_body=RegistrationSerializer,
        responses=dummy_api_response.student_registerview_response_schema_dict,
    )
    def post(self, request):
        posted_data = request.data
        serializer = self.serializer_class(data=posted_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_payload = {
            "status": "User Created Successfully",
            "message": "Login with your staff ID and the Default Password",
        }

        return Response(response_payload, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = (CustomAPIResponseRenderer,)

    @swagger_auto_schema(
        operation_summary="Account Login",
        operation_description="Login in with username/email and password and receive tokens(with user data)",
        responses=dummy_api_response.loginview_response_schema_dict,
    )
    def post(self, request):
        """
        Perform user login.

        Authenticates the user based on the provided credentials.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The response indicating the result of user login.

        Raises:
            AuthenticationFailed: If the provided credentials are invalid or the user account is disabled

        """
        serializer = self.serializer_class(data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)

        if is_valid:
            validated_data = serializer.validated_data
            return Response(validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom implementation of the TokenRefreshView class.



    Attributes:
        renderer_classes (tuple): A tuple of renderer classes for custom API response rendering.
                                  This allows control over the structure and format of the response sent to the client.

    """

    renderer_classes = (CustomAPIResponseRenderer,)

    @swagger_auto_schema(
        operation_summary="Refresh Existing Token",
        operation_description="Access already Existing token, and \n"
        "returns new authentication tokens (access and refresh)",
        responses=dummy_api_response.refresh_token_response_schema_dict,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    renderer_classes = (CustomAPIResponseRenderer,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Change Password When User is Logged In",
        operation_description="It accepts old password and new password to update the user password. \n"
        " After a successful password update, user jwt tokens is being deleted and requires a new login",
        responses=dummy_api_response.change_password_response_schema_dict,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Check if the old password matches the one in the database
            if not check_password(old_password, user.password):
                return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password with the new one
            user.set_password(new_password)
            user.save()

           # Deleting User Token after password changing.
            OutstandingToken.objects.get(user=request.user).delete()


            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
