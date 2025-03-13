from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings

# rest_framework
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='api/v1/schema/swagger-ui/')),
    
    path('api/v1/', include('api.urls')),

    # simple jwt
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # swagger
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),

]

# Only show Swagger if not in production
if settings.ENVIRONMENT != 'production':
    
    urlpatterns += [
        path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

