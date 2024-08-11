from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts import utils as account_utils
from accounts.throttling import PhoneRateThrottle

User = get_user_model()


class PhoneNumberVerificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [PhoneRateThrottle, AnonRateThrottle]

    @swagger_auto_schema(
        operation_summary="Send OTP to phone number",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number of the user'),
            },
            required=['phone']
        ),
        responses={
            200: openapi.Response(
                description="OTP sent successfully",
                examples={
                    'application/json': {
                        'error': False,
                        'message': 'An OTP token has been sent to your phone number. Please use it to register.',
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    'application/json': {
                        'error': True,
                        'errors': 'Failed to generate OTP. Please try again.',
                    }
                }
            ),
            403: openapi.Response(
                description="User is already logged in",
                examples={
                    'application/json': {
                        'error': True,
                        'message': 'You are already logged in.',
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    'application/json': {
                        'error': True,
                        'message': 'User does not exist. Please register first.',
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
        data = request.data
        phone = data.get("phone")
        try:
            user = User.objects.get(phone=phone)
            otp_key = account_utils.generate_random_digits(6)
            otp_value = user.phone
            redis_response = account_utils.set_to_redis(key=otp_key, value=otp_value, database='OTP')
            if not redis_response:
                return Response(
                    {"error": True, "errors": redis_response}, status=status.HTTP_400_BAD_REQUEST)
            # since there is not otp service I'll send otp throw response
            return Response(
                {'error': False,
                 "message": f"An otp token has send to your phone number please use it to register. token{otp_key}"},
                status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': True, "message": 'User does not exist. Please register first.'},
                            status=status.HTTP_404_NOT_FOUND)
