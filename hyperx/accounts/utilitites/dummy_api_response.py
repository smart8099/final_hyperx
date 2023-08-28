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


loginview_response_schema_dict = {
    "200": openapi.Response(
        description="Successful Login",
        examples={
            "application/json": {
                "data": {
                    "staff_id": "01210884B",
                    "user_role": "NURSE",
                    "change_default_password": "True",
                    "tokens": {
                        "refresh": "4i@n&IaZo^)M_0+#6Hv!sLRfKteqBY8Wxj2DlQXkUb$GO-JpVuy7PC.FS3Z59TrwhmgcNE1dJzv*A~@(;`",
                        "access": "l-$nG6*RdqH;Yeo9LXaI5ECtyKv.>P`+VpW2sbOZ8Q7FAJ~{4!@DzMsx&[N[3BUciGTYXUKw1m%jh4a_#vrnS=)>,[};u",
                    },
                }
            }
        },
    ),
    "401": openapi.Response(
        description="Invalid Credentials",
        examples={"application/json": {"errors": {"detail": "Invalid credentials, try again"}}},
    ),
}


refresh_token_response_schema_dict = {
    "201": openapi.Response(
        description="Successful Token Refresh",
        examples={
            "application/json": {
                "data": {
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5MTY5MDE4LCJpYXQiOjE2ODkxNjQ2NTEsImp0aSI6Ijc5NDQ2ZmU1NzA5OTRhNjY4MmFhOTQ5OWU2Y2JhNTc3IiwidXNlcl9pZCI6MX0.jElOtDh06A-yj-YbW7Va7Rfpuhj5U5E38rqnKzCQ7XQ",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTI1MTgxOCwiaWF0IjoxNjg5MTY1NDE4LCJqdGkiOiIwZjVkZjJiYjkzNjE0NmIyYTYyN2NhNDNlNzI5NGE0ZiIsInVzZXJfaWQiOjF9.Z3hSBOGEAyWsZLsDN3xBdH8WlVr8WfBxu0LKWqJkI5o",
                }
            }
        },
    ),
    "401": openapi.Response(
        description="Invalid Refresh Token/Unauthorized",
        examples={
            "application/json": {
                "errors": {
                    "detail": "Token is invalid/blacklisted or expired",
                    "code": "token_not_valid",
                }
            }
        },
    ),
    "403": openapi.Response(
        description="Forbidden Access",
        examples={"application/json": {"errors": {"detail": "You do not have permission to perform this action."}}},
    ),
}
