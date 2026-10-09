from django.urls import path
from rest_framework_simplejwt .views import TokenObtainPairView, TokenRefreshView

from .api_views import UserAPIView, UserByIdView, ProviderProfileByIdView, MeView, ProviderProfileView, UsergetAPIView, SelectRoleAPIView 

urlpatterns = [
    
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh/token", TokenRefreshView.as_view(), name="refresh_token"),
    path("auth/me/", MeView.as_view(), name="auth"),
    path("users/", UserAPIView.as_view(), name="user"),
    path("users/profile/",UsergetAPIView.as_view(),name="get"),
    path("users/<int:id>/", UserByIdView.as_view(), name="userbyID"),
    path("provider/",ProviderProfileView.as_view(),name="provider"),
    path("users/<int:user_id>/provider-profile", ProviderProfileByIdView.as_view(), name="providerbyid"),
    path("select-role/", SelectRoleAPIView.as_view(), name="select_role"),

]
