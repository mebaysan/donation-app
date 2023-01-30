"""donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API URLs
    path('api/', include('apps.web.api.urls')),
    # AUTH ENDPOINTS
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # API Doc
    path('api/openapi/', get_schema_view(
        title=settings.APP_NAME,
        description="API Documentation",
        version="1.0.0",
        patterns=[
            path('api/', include('apps.web.api.urls')),
            path('api/token/', TokenObtainPairView.as_view()),
            path('api/token/refresh/', TokenRefreshView.as_view()),
            path('api/token/verify/', TokenVerifyView.as_view()),
        ]
    ), name='openapi-schema'
         ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG == 1:
#     urlpatterns += path('api/auth/', include('rest_framework.urls')),
