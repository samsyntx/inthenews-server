from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dotenv import load_dotenv
from django.conf import settings
import os
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import RegisterAPI, ConfirmEmailAPI, ResendOTPAPI, LoginAPIView, HomeAPI, ProfileAPIView
from apis.views import PaginatedBlogListAPIView, BlogCreateAPIView, BlogLatestThreeAPIView, BlogExceptLatestThreeAPIView, BlogDetailAPIView

load_dotenv()

schema_view = get_schema_view(
    openapi.Info(
        title="INTHENEWS",
        default_version='v1',
        description="API documentation for your Django project",
        terms_of_service="https://www.yourproject.com/terms/",
        contact=openapi.Contact(email="contact@yourproject.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', HomeAPI.as_view(), name='home'),
    path('auth/register/', RegisterAPI.as_view(), name='register'),
    path('auth/confirm-email/', ConfirmEmailAPI.as_view(), name='confirm-email'),
    path('auth/resend-otp/', ResendOTPAPI.as_view(), name='resend-otp'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),

    path('profile/', ProfileAPIView.as_view(), name='profile'),

    path('blog/create/', BlogCreateAPIView.as_view(), name='create-blog'),
    path('blogs/latest/', BlogLatestThreeAPIView.as_view(), name='latest-blogs'),
    path('blogs/except-latest/', BlogExceptLatestThreeAPIView.as_view(), name='except-latest-blogs'),
    path('blogs/', PaginatedBlogListAPIView.as_view(), name='paginated-blogs'),  
    path('blogs/<int:id>/', BlogDetailAPIView.as_view(), name='blog_detail'),
]

if settings.DEBUG or os.getenv('SHOW_SWAGGER_IN_PRODUCTION', 'False') == 'True':
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
