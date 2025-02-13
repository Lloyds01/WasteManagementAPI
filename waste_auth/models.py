import pytz
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _
from .managers import UserManager, OTPManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .helpers.reusable import validate_password, email_sender
from .enums import GenderChoices, UserType


# Create your model(s) here.
class BaseModel(models.Model):
    """Base model for reuse.
    Args:
        models (Model): Django's model class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user profile.
    """
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    email_verified = models.BooleanField(default=False)
    password = models.CharField(
        max_length=255, validators=[validate_password], editable=False
    )
    phone_number = models.CharField(max_length=25, unique=True)
    phone_verified = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    user_type = models.CharField(max_length=12, choices=UserType.choices, default=UserType.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "USER PROFILE"
        verbose_name_plural = "USERS PROFILE"

    def __str__(self) -> str:
        return self.email

    def get_fullname(self) -> str:
        """
        Returns the full name of the person.
        If both the first name and last name are available,
        it concatenates them with a space in between and returns the full name.
        If either the first name or last name is missing, it returns None.
        Returns:
            str: The full name of the person, or None if first name or last name is missing.
        """
        if not self.first_name or not self.last_name:
            return None
        else:
            return f"{self.first_name} {self.last_name}"


    @classmethod
    def sign_up(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        password: str
    ) -> bool:
        """
        Validates and creates a new user instance.
        Args:
            cls (class): The class reference for the user model.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email address of the user.
            phone_number (str): The phone number of the user.
            password (str): The password for the user.
            is_investor (bool): Optional. Whether the user is an investor. Default is False.
            is_account_manager (bool): Optional. Whether the user is an account manager. Default is False.
        Returns:
            bool: True if the user instance is created successfully.

        """
        user = cls.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=password
        )
        otp = OTP.get_otp(
            type="EMAIL VERIFICATION",
            recipient=email,
            length=6,
            expiry_time=10
        )
        print(otp, "TESTING OTP GENERATOR")
        send_email = email_sender(
            recipient=[user.email],
            subject="Welcome Onboard",
            text=f"""
Hello {user.first_name.capitalize()},\n
Thank you for registering on our platform! Please verify your account by entering this code below:\n
{otp}\n\n
Best regards,\n
The Team at WasteBoard.
            """
        )
        return user

    @classmethod
    def sign_in(cls, email: str, password: str) -> dict or None:
        """
        Authenticates a user with the provided email and password, generating a token for successful sign-in.
        Args:
            cls (class): The class reference for the user model.
            email (str): The email address of the user.
            password (str): The password of the user.
        Returns:
            dict or None: A dictionary containing sign-in information if successful, or None if authentication fails.
                - status (bool): The status of the sign-in attempt (True for success, False otherwise).
                - user (int): The ID of the authenticated user.
                - access (str): The access token for the authenticated user.
                - message (str): (Optional) A message indicating that the user profile is not verified.
        """
        user = authenticate(email=email, password=password)
        # print(user, "USER EMAIL INFORMATION")
        if user is not None:
            if not user.email_verified:
                return {"message": "USER PROFILE is not verified."}
            token = RefreshToken.for_user(user)
            user.last_login = datetime.now(
                tz=pytz.timezone(settings.TIME_ZONE)
            )
            user.save()

            data = {
                "status": True,
                "user": user.id,
                "access": str(token.access_token),
                "refresh": str(token)
            }
            return data
        return None


    @classmethod
    def change_password(cls, user: isinstance, old_password: str, new_password: str) -> dict:
        """
        Change the password of a user.
        Args:
            cls (class): The class reference for the user model.
            user (object): The user object for which the password will be changed.
            old_password (str): The old password entered by the user.
            new_password (str): The new password to be set for the user.
        Returns:
            dict: A dictionary containing a message indicating the status of the password change.
        """
        if user:
            verify_password = check_password(old_password, user.password)
            if verify_password:
                # crosscheck passwords for similarities
                if old_password == new_password:
                    return {"message": "similar password, try a new one."}
                user.set_password(new_password)
                user.save()
                return {"message": "password changed successfully."}
            return {"message": "old password is incorrect, forgot password?"}
        return {"message": "user does not exist."}



    @classmethod
    def forgot_password(cls, email: str = None, phone_number: str = None) -> dict:
        """
        Send a password reset OTP to the user's email or phone number.
        Args:
            email (str): User's email address for password reset. Defaults to None.
            phone_number (str): User's phone number for password reset. Defaults to None.
        Returns:
            dict: A dictionary containing the status and message of the operation.
                - status (bool): True if OTP sent successfully, False otherwise.
                - message (str): Message describing the outcome of the operation.
        """
        if email is not None:
            user = cls.objects.filter(email=email).first()
            if user is not None:
                otp = OTP.get_otp(
                    type="PASSWORD RESET",
                    recipient=email,
                    length=6,
                    expiry_time=10
                )
                print(otp, "OTP")
                send_email = email_sender(
                    recipient=[email],
                    subject="Password Reset",
                    text=f"""
                Hello {user.first_name.capitalize()},\n
                A password reset was requested on your account, complete the process with the code below:\n
                {otp}\n
                Kindly disregard this email if you didn't request one.\n\n
                Best regards,\n
                The Team at Liberty Tech X.

                    """
                )
                print(send_email)
                return {
                    "status": True,
                    "message": "OTP has been sent to your registered email."
                }
            return {
                "status": False,
                "message": "USER PROFILE does not exist."
            }

        if phone_number is not None:
            pass

    @classmethod
    def reset_password(cls, otp: str, new_password: str, email: str = None, phone_number: str = None):
        """
        Set a new password for an existing user.
        Args:
            cls (class): The class reference for the user model.
            otp (str): One time password used for verification.
            new_password (str): The new password to be set for the user.
            email (str): User's email address for password reset. Defaults to None.
            phone_number (str): User's phone number for password reset. Defaults to None.
        Returns:
            dict: A dictionary containing the status and message of the operation.
                - status (bool): True if password reset was successful, False otherwise.
                - message (str): Message describing the outcome of the operation.
        """
        verify = OTP.verify_otp(
            recipient=email if email is not None else phone_number,
            otp=otp
        )
        if verify.get("status") == True:
            if email is not None:
                user = cls.objects.filter(email=email).first()
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    return {
                        "status": True,
                        "message": "password reset was successful."
                    }
                return {
                    "status": False,
                    "message": "USER PROFILE does not exist."
                }

            if phone_number is not None:
                pass
        return {
            "status": False,
            "message": "invalid or expired OTP."
        }

    @classmethod
    def update_user_details(
        cls,
        user,
        first_name: str = None,
        middle_name: str = None,
        last_name: str = None,
        address: str = None
    ):
        """
        Update the details of a user object based on the provided parameters.
        Args:
            cls (class): The class reference for the user model.
            user (User): The User object.
            first_name (str): The new first name of the user.
            middle_name (str): The new middle name of the user.
            last_name (str): The new last name of the user.
            address (str): The new address of the user.
        Returns:
            user: If the user is found and updated successfully, returns the updated user object.
            None: If the user is not found or inactive, returns None.
        """
        user = cls.objects.filter(email=user.email, is_active=True).first()
        if user is not None:
            user.first_name = first_name if first_name is not None else user.first_name
            user.middle_name = middle_name if middle_name is not None else user.middle_name
            user.last_name = last_name if last_name is not None else user.last_name
            user.address = address if address is not None else user.address
            user.save()
            return user
        return None

class OTP(BaseModel):
    """
    Model representing a One-Time Password (OTP).
    Attributes:
        type (str): The type of the OTP (e.g., "registration", "password-reset", etc.).
        recipient (str): The recipient's identifier (e.g., email address, phone number).
        length (int): The length of the OTP code.
        expiry_time (int): The validity period of the OTP in seconds.
        code (str): The generated OTP code.
        is_used (bool): Flag indicating whether the OTP has been used or not.
    Relationships:
        objects (OTPManager): Custom manager for OTP objects.
    """
    type = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    length = models.IntegerField()
    expiry_time = models.IntegerField()
    code = models.CharField(max_length=255)
    is_used = models.BooleanField(default=False)

    objects = OTPManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "ONE TIME PASSWORD"
        verbose_name_plural = "ONE TIME PASSWORDS"

    def __str__(self) -> str:
        return f"{self.type} OTP sent to {self.recipient}"

    @property
    def time_valid(self):
        """
        Property that checks if the object's created time is still within the valid time range.
        Returns:
            bool: True if the object's created time is within the valid time range, False otherwise.
        """
        current_time = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        return True if self.created_at > current_time - timedelta(minutes=self.expiry_time) else False

    @classmethod
    def get_otp(
        cls,
        type: str,
        recipient: str,
        length: int = 6,
        expiry_time: int = 5
    ):
        """
        Generate and retrieve a new OTP (One-Time Password) object.
        Args:
            type (str): The type of the OTP.
            recipient (str): The recipient of the OTP.
            length (int, optional): The length of the OTP. Defaults to 6.
            expiry_time (int, optional): The expiry time of the OTP in minutes. Defaults to 5.
        Returns:
            OTP: The newly created OTP object.
        """
        otp = cls.objects.create_otp(
            type=type,
            recipient=recipient,
            length=length,
            expiry_time=expiry_time
        )
        return otp

    @classmethod
    def verify_otp(cls, recipient: str, otp: str) -> dict:
        """
        Verify the OTP (One-Time Password) for the given recipient.
        Args:
            recipient (str): The recipient for whom to verify the OTP.
            otp (str): The OTP to be verified.
        Returns:
            dict: A dictionary containing the verification status and message.
                - If the OTP is valid and not expired, the status will be True and the message will be "OTP is valid for recipient."
                - If the OTP is invalid or expired, the status will be False and the message will be "invalid or expired OTP."
                - If no valid OTP is found for the recipient, the status will be False and the message will be "invalid or expired OTP."
        """
        one_time_password = cls.objects.filter(
            recipient=recipient, is_used=False).first()
        if one_time_password is not None:
            if one_time_password.time_valid:
                verified = check_password(otp, one_time_password.code)
                if verified:
                    one_time_password.is_used = True
                    one_time_password.save()
                    return {"status": True, "message": "OTP is valid for recipient."}
                return {"status": False, "message": "invalid or expired OTP."}
            return {"status": False, "message": "invalid or expired OTP."}
        return {"status": False, "message": "invalid or expired OTP."}



# class WasteProducts(models.Model):

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_products')
#     waste_type = models.CharField(max_length=50, choices=WASTE_TYPES)
#     quantity = models.PositiveIntegerField()
#     weight = models.FloatField(null=True, blank=True)  # Optional field
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-created_at"]
#         verbose_name = "RECYCLE PRODUCT"
#         verbose_name_plural = "RECYCLE PRODUCT"

#     def __str__(self):
#         return f"{self.waste_type} - {self.quantity} units"