from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts import serializers as account_serializers

User = get_user_model()


class RegisterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = account_serializers.UserInfoSerializer

    @swagger_auto_schema(
        operation_summary="Update user profile",
        request_body=account_serializers.UserInfoSerializer,
        responses={
            200: openapi.Response(
                description="User profile updated successfully",
                schema=account_serializers.UserInfoSerializer
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    'application/json': {
                        'error': True,
                        'message': 'Invalid data'
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized",
                examples={
                    'application/json': {
                        'error': True,
                        'message': 'Authentication credentials were not provided.'
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"error": False, 'data': serializer.data}, status=status.HTTP_201_CREATED)
