from rest_framework import serializers

from .helpers.reusable import validate_password
from .enums import UserType
from .models import User


# Create your serializer(s) here.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        write_only=True
    )
    confirm_password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            # "user_type",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "confirm_password"
        ]

    def validate(self, attrs):

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"detail": "password(s) do not match."}
            )
        attrs.pop("confirm_password")
    
        return attrs


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        write_only=True
    )

class IndustryCreateSerializer(serializers.Serializer):
    industry_name = serializers.ListField(required=True,
    child=serializers.CharField(max_length=255),
    allow_empty=False
    )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        write_only=True
    )
    new_password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        write_only=True
    )
    confirm_password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        write_only=True
    )

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"detail": "new password(s) do not match."}
            )
        attrs.pop("confirm_password")
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def validate(self, attrs):
        if not attrs.get("email") or attrs.get("phone_number"):
            raise serializers.ValidationError(
                {"detail": "input a valid email or phone number."}
            )
        return attrs


class UserVerificationSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class UserUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    address = serializers.CharField(required=False)


class UserPasswordResetSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    new_password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        write_only=True
    )
    confirm_password = serializers.CharField(
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
        write_only=True
    )

    def validate(self, attrs):
        if not attrs.get("email") or attrs.get("phone_number"):
            raise serializers.ValidationError(
                {"detail": "input a valid email or phone number."}
            )
        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"detail": "new password(s) do not match."}
            )
        attrs.pop("confirm_password")
        return attrs
