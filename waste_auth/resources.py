from import_export import resources
from .models import *


class UserResource(resources.ModelResource):
    class Meta:
        model = User

class OTPResource(resources.ModelResource):
    class Meta:
        model = OTP