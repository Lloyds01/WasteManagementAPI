from django.contrib.auth.models import BaseUserManager
from pyotp.totp import TOTP
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.db import models
from .helpers.reusable import convert_string_to_base32


# Create your manager(s) here.
class OTPManager(models.Manager):
    """
    Handles OTP generation.
    OTP is unique per user as the user identifier is used as secret.
    """
    SECRET = settings.OTP_SECRET

    def create_otp(
        self,
        type: str,
        recipient: str,
        length: int,
        expiry_time: int
    ):
        """
        Create a One-Time Password (OTP) and store it in the database.
        Args:
            type (str): The type of OTP being generated, e.g., "email" or "phone".
            recipient (str): The recipient's identifier for whom the OTP is being generated.
            length (int): The length of the OTP to be generated.
            expiry_time (int): The validity time of the OTP in seconds.
        Returns:
            str: The generated OTP code as a string.
        Raises:
            None
        """
        code_generator = TOTP(
            convert_string_to_base32(f"{self.SECRET};{recipient}"),
            digits=length
        )
        code_value = code_generator.now()

        otp = self.model(
            type=type,
            recipient=recipient,
            length=length,
            expiry_time=expiry_time,
            code=make_password(code_value)
        )
        otp.save()
        return code_value


# Create your manager(s) here.
class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.
    """

    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a user with the given email and password.
        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields: Additional fields for the user model.
        Returns:
            User: The newly created user object.
        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError('Users must provide a valid email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a regular user with the given email and password.s
        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields: Additional fields for the user model.
        Returns:
            User: The newly created user object.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a superuser with the given email and password.
        Args:
            email (str): The email address of the user.
            password (str): The password for the superuser.
            **extra_fields: Additional fields for the user model.
        Returns:
            User: The newly created superuser object.
        Raises:
            ValueError: If the is_staff or is_superuser fields are not set to True.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self._create_user(
            email,
            password,
            **extra_fields
        )