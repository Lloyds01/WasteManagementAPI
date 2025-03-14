from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


# Swagger-UI.
schema_view = get_schema_view(
    openapi.Info(
        title="WASTE MANAGEMENT API",
        default_version='v1.0',
        description="Basic Auth API for Waste Management System",
        terms_of_service="",
        contact=openapi.Contact(email="segzyoly@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny, ],
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0)),
    path('admin/', admin.site.urls),
    path('user_auth/', include('waste_auth.urls')),
    # path('transactions/', include('account.urls')),

]





