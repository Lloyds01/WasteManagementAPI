from import_export import resources
from .models import *


class UserResource(resources.ModelResource):
    class Meta:
        model = User

class OTPResource(resources.ModelResource):
    class Meta:
        model = OTP

class AgentAssignmentResource(resources.ModelResource):
    class Meta:
        model = AgentAssignment

class WasteProductResource(resources.ModelResource):
    class Meta:
        model = WasteProduct