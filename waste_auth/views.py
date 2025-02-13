from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, OTP
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserVerificationSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    UserPasswordResetSerializer,
    IndustryCreateSerializer,
)

# Create your view(s) here.
class UserSignUpAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.sign_up(**serializer.validated_data)
        if user:
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(errors=serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

class UserVerificationAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify = OTP.verify_otp(**serializer.validated_data)
        user = User.objects.filter(email=serializer.validated_data.get("recipient")).last()
        if verify.get("status") == True:
            user.email_verified=True
            user.save()
            return Response(data=verify, status=status.HTTP_200_OK)
        return Response(data=verify, status=status.HTTP_400_BAD_REQUEST)


class UserSignInAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.sign_in(**serializer.validated_data)
        if user is not None:
            if user.get("status") == True:
                return Response(data=user,  status=status.HTTP_200_OK)
            return Response(data=user,  status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            return Response(
                data={"message": "invalid credentials (wrong email or password)."},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fields_to_be_updated = serializer.validated_data.items()
        if len(fields_to_be_updated) > 0:
            profile_update = User.update_user_details(
                user=request.user, **serializer.validated_data
            )
            if profile_update is not None:
                serializer = UserSerializer(instance=profile_update)
                return Response(
                    data=serializer.data, status_code=200, status=status.HTTP_200_OK
                )
            return Response(
                errors={"message": "USER PROFILE does not exists."}, status_code=400, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            errors={"message": "no field(s) was passed to be updated."}, status_code=400,
            status=status.HTTP_400_BAD_REQUEST
        )


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = User.change_password(
            user=request.user, **serializer.validated_data
        )
        return Response(data=password, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        forgot_password = User.forgot_password(**serializer.validated_data)
        if forgot_password.get("status") == True:
            return Response(data=forgot_password, status=status.HTTP_200_OK)
        return Response(data=forgot_password, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password = User.reset_password(**serializer.validated_data)
        if reset_password.get("status") == True:
            return Response(data=reset_password, status_code=200, status=status.HTTP_200_OK)
        return Response(data=reset_password, status=status.HTTP_400_BAD_REQUEST)


class IndustryCreateAPIView(APIView):
    def post(self, request):
        serializer = IndustryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        industries = serializer.validated_data['industry_name']
        # Fetch existing industry names
        existing_names = set(Industry.objects.values_list('industry_name', flat=True))
        new_industries = [industry_name for industry_name in industries if industry_name not in existing_names]

        # Bulk create industries with the correct field name
        Industry.objects.bulk_create([Industry(industry_name=industry_name) for industry_name in new_industries])
        
        return Response({
            "created": new_industries,
            "existing": list(set(industries) - set(new_industries))
        }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
