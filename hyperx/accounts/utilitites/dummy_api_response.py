from drf_yasg import openapi

student_registerview_response_schema_dict = {
    "200": openapi.Response(
        description="Student Successfully Registered",
        examples={"application/json": {"data": {"success": "User Created Successfully"}}},
    ),
    "400": openapi.Response(
        description="Bad Request",
        examples={
            "application/json": {
                "errors": {
                    "username": ["This username is already taken"],
                    "email": ["This email is already taken"],
                    "error": ["Passwords do not match."],
                    "field_name": ["This field may not be blank."],
                }
            }
        },
    ),
}
