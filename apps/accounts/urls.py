from . views import UserAPIView,UserByIdView,ProviderProfileByIdView
from django.urls import path


urlpatterns = [
    path("users/", UserAPIView.as_view(), name="user"),
    path("users/<int:id>", UserByIdView.as_view(), name="userbyID"),
    path("users/<int:user_id>/provider-profile", ProviderProfileByIdView.as_view(), name="providerbyid")
]
