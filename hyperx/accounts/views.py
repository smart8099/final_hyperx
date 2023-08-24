from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hyperx.utils.renderer import CustomAPIResponseRenderer

from .serializers import RegistrationSerializer
from .utilitites import dummy_api_response


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
