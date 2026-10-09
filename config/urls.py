"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import include, path, re_path

from apps.accounts.api_views import GoogleLogin, GoogleLoginCallback 

API_PREFIX = "api"

urlpatterns = [

    path('admin/', admin.site.urls),
    path(f"{API_PREFIX}/accounts/", include("apps.accounts.urls")),
    path(f"{API_PREFIX}/services/", include("apps.services.urls")),
    path(f"{API_PREFIX}/bookings/", include("apps.bookings.urls")),
    path(f"{API_PREFIX}/ratings/", include("apps.ratings.urls")),


    path("", include("apps.core.urls")),
    path('accounts/', include('allauth.urls')),

    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("api/v1/auth/google/callback/",GoogleLoginCallback.as_view(), name="google_login_callback",),
    
    
]
