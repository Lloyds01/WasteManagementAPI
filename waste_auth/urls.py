from django.urls import path
from .views import *

# Create your url pattern(s) here.
urlpatterns = [
    path("register/", UserSignUpAPIView.as_view()),
    path("register-agent/", AgentSignUpAPIView.as_view()),
    path("verify_otp/", UserVerificationAPIView.as_view()),
    path("login/", UserSignInAPIView.as_view()),
    path("details/", UserDetailsAPIView.as_view()),
    path("change-password/", ChangePasswordAPIView.as_view()),
    path("forgot-password/", ForgotPasswordAPIView.as_view()),
    path("otp-reset-password/", ResetPasswordAPIView.as_view()),
    path("product/", wasteProductAPIView.as_view()),
]


