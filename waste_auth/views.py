from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import AccountSystem, Wallet
from waste_auth.enums import AccountType
from .models import( User, OTP, WasteProduct)
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserVerificationSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    UserPasswordResetSerializer,
    WasteProductSerializer,
    UserUpdateSerializer
)
from .enums import UserType

# Create your view(s) here.
class UserSignUpAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.sign_up(**serializer.validated_data)
        if user:
            response_data = {
            "status": 201,
            "message": "User created successfully",
            "data": {
                "first_name": serializer.validated_data.get("first_name"),
                "middle_name": serializer.validated_data.get("middle_name"),
                "last_name": serializer.validated_data.get("last_name"),
                "email": serializer.validated_data.get("email"),
                "phone_number": serializer.validated_data.get("phone_number"),
                "user_type": user.user_type,
            }
        }
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(errors=serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class AgentSignUpAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.sign_up(**serializer.validated_data)
        if user:
            user.user_type = "AGENT"
            user.save()
            response_data = {
            "status": 201,
            "message": "User created successfully",
            "data": {
                "first_name": serializer.validated_data.get("first_name"),
                "middle_name": serializer.validated_data.get("middle_name"),
                "last_name": serializer.validated_data.get("last_name"),
                "email": serializer.validated_data.get("email"),
                "phone_number": serializer.validated_data.get("phone_number"),
                "user_type": user.user_type,
            }
        }
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(errors=serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

class UserVerificationAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verify = OTP.verify_otp(**serializer.validated_data)
        user = User.objects.filter(email=serializer.validated_data.get("recipient")).last()
        if verify.get("status") == True:
            create_acct = AccountSystem.create_account(
                user=user,
                account_name=user.first_name + " " + user.last_name,
                account_type=AccountType.COLLECTION,
                account_provider="VFD",
                bank_name="VFD Microfinance Bank",
                bank_code="999999"
            )
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
        response_data = {
            "status": 200,
            "message": "User Details",
            "data": {
                "first_name": user.first_name,
                "middle_name": user.middle_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "email_verified": user.email_verified,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

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


class wasteProductAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = WasteProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.user_type is UserType.AGENT:
            return Response(
                data={"message": "Only users can create products"},
                status=status.HTTP_400_BAD_REQUEST)

        if user.address is None:
            return Response(
                data={"message": "Please update your profile to add address to help with product collection"},
                status=status.HTTP_400_BAD_REQUEST
            )
        product = WasteProduct.create_product(user=user, **serializer.validated_data)
        if product:
            response_data = {
                "status": 201,
                "message": "Product created successfully",
                "data": {
                    "product": serializer.validated_data.get("waste_type"),
                    "quantity": serializer.validated_data.get("quantity"),
                    "weight": serializer.validated_data.get("weight"),
                }
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(errors=serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data.get("address")
        bvn = serializer.validated_data.get("bvn")
        user = request.user
            
        user.bvn=bvn
        user.address=address
        user.save()
        response_data = {
                "status": 201,
                "message": "Profile updated successfully",
                "data":{
                    "address":user.address,
                    "bvn": user.bvn
                }
                }
        
        return Response(response_data, status=status.HTTP_200_OK)



