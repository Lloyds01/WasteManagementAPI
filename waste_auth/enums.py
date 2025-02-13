from django.db import models
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class UserType(TextChoices):
    AGENT = "AGENT", "agent"
    USER = "USER", "user"
  

class GenderChoices(TextChoices):
    MALE = "MALE", "male"
    FEMALE = "FEMALE", "female"