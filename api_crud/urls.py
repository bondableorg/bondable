from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Bondable API",
      default_version='v1',
      description="First version of the Bondable API",
      terms_of_service="",
      contact=openapi.Contact(email="info@bondable.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# urls
urlpatterns = [
    path("api/v1/homes/", include("homes.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/auth/", include("authentication.urls")),
    
    path("admin/", admin.site.urls),
    path("", views.index, name="dashboard"),
    path('playground/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]
