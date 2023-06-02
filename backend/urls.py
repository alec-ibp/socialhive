from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


docs_urls = [
    # Optional UI:
    path('schema/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('schema/file', SpectacularAPIView.as_view(), name='schema'),
]

urls_jwttoken = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

common_urls = [
    path('', include('socialhive.common.urls')),
]

urlpatterns = [
    path('', include(urls_jwttoken)),
    path('admin/', admin.site.urls),
    path('docs/', include(docs_urls)),
    path('api/v1/', include(common_urls)),
]
