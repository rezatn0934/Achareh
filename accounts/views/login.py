# views.py
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.throttling import PhoneRateThrottle

User = get_user_model()


class LoginView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [PhoneRateThrottle, AnonRateThrottle]
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="Login user and obtain JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    'application/json': {
                        "error": False,
                        "token": {
                            "access": "string",
                            "refresh": "string"
                        }
                    }
                }
            ),
            403: openapi.Response(
                description="User is already logged in",
                examples={
                    'application/json': {
                        "error": True,
                        "message": "You are already logged in."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    'application/json': {
                        "error": True,
                        "message": "Invalid username or password."
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {"error": True, "message": "You are already logged in."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = serializer.validated_data

        return Response({'error': False, "token": tokens}, status=status.HTTP_200_OK)
