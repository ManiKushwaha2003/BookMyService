from . views import UserAPIView,UserByIdView,ProviderProfileByIdView
from django.urls import path
from rest_framework_simplejwt .views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh/token", TokenRefreshView.as_view(), name="refresh_token"),
    path("users/", UserAPIView.as_view(), name="user"),
    path("users/<int:id>", UserByIdView.as_view(), name="userbyID"),
    path("users/<int:user_id>/provider-profile", ProviderProfileByIdView.as_view(), name="providerbyid")
]
