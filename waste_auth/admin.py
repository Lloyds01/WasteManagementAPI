from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import DateFieldListFilter
from .resources import *

# Register your models here.
class UserResourceAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    search_fields = ("",)
    list_filter = (
        ("created_at", DateFieldListFilter),
        "email",
        "phone_number",
    )

    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

class OTPResourceAdmin(ImportExportModelAdmin):
    resource_class = OTPResource
    search_fields = ("",)
    list_filter = (
        ("created_at", DateFieldListFilter),
    )

    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

class AgentAssignmentResourceAdmin(ImportExportModelAdmin):
    resource_class = AgentAssignmentResource
    search_fields = ("",)
    list_filter = (
        ("created_at", DateFieldListFilter),
    )

    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

class WasteProductResourceAdmin(ImportExportModelAdmin):
    resource_class = WasteProductResource
    search_fields = ("",)
    list_filter = (("created_at", DateFieldListFilter),
    )

    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

class RecycleAgentsResourceAdmin(ImportExportModelAdmin):
    resource_class = RecycleAgentsResource
    search_fields = ("",)
    list_filter = (("created_at", DateFieldListFilter),
    )

    def get_list_display(self, request):
        data = [field.name for field in self.model._meta.concrete_fields]
        return data

admin.site.register(User, UserResourceAdmin)
admin.site.register(WasteProduct, WasteProductResourceAdmin)
admin.site.register(AgentAssignment, AgentAssignmentResourceAdmin)
admin.site.register(OTP, OTPResourceAdmin)
admin.site.register(RecycleAgents, RecycleAgentsResourceAdmin)