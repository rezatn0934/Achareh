from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from accounts import utils as account_utils

User = get_user_model()


class ValidateOTP(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Validate OTP and create user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='One-time password (OTP)'),
            },
            required=['otp']
        ),
        responses={
            200: openapi.Response(
                description="Access token generated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Error status'),
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Generated JWT access token')
                    },
                    required=['error', 'access_token']
                )
            ),
            404: openapi.Response(
                description="Invalid OTP",
                examples={
                    'application/json': {
                        'error': True,
                        'errors': 'captcha is invalid.'
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        otp = data.get('otp')
        response = account_utils.get_from_redis(database='OTP', key=otp)
        if not response:
            return Response({"error": True, "errors": 'Otp is invalid.'}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.create_user(phone=response, is_active=False)
        access_token = str(AccessToken.for_user(user))
        return Response({'error': False, "access_token": access_token}, status=status.HTTP_200_OK)
