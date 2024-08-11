from django.urls import path
from .views import login, validate_otp, register, phone_verification

urlpatterns = [
    path('login/', login.LoginView.as_view(), name='login'),
    path('validate-otp/', validate_otp.ValidateOTP.as_view(), name='validate-otp'),
    path('register/', register.RegisterView.as_view(), name='register'),
    path('phone-verification/', phone_verification.PhoneNumberVerificationView.as_view(), name='phone-verification')
]
