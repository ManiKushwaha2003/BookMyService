from django.shortcuts import render
from django.urls import path

from apps.accounts.views import home, login, register, userdashboard, providerdashboard, createbooking, profile, booking_offers, my_booking, rating, provider_profile, request, provider_offer, provider_work, addservice, userlist
from apps.accounts.views import userupdate, userview , selectrole , GoogleCallbackRender , CustomerDetail





# Create your views here.

ACCOUNTS_PREFIX = "accounts"

urlpatterns = [
    path("", home.as_view(),name="home"),
    path(f"{ACCOUNTS_PREFIX}/user/login/", login.as_view(), name="login"),
    path(f"{ACCOUNTS_PREFIX}/user/register/", register.as_view(), name="register"),
    path(f"{ACCOUNTS_PREFIX}/google/callback", GoogleCallbackRender.as_view(), name="google"),

    
    path("user-dashboard/", userdashboard.as_view(), name="user_dashboard"),
    path("provider-dashboard/", providerdashboard.as_view(), name="user_dashboard"),
    path("create-booking/", createbooking.as_view(), name="create"),
    path("profile/", profile.as_view(),name="profile"),
    path("booking_offers/",booking_offers.as_view(),name="bookingoffers"),
    path("my_booking/",my_booking.as_view(),name="mybooking"),
    path("rating/<int:id>/",rating.as_view(),name="rating"),
    path("add-service/",addservice.as_view(),name="rating"),
    path("user-list/",userlist.as_view(),name="userlist"),
    path("user-update/<int:id>/",userupdate.as_view(),name="userupdate"),
    path("user-view/<int:id>/",userview.as_view(),name="userupdate"),

 
    path("provider_profile/",provider_profile.as_view(),name="providerprofile"),
    path("request/",request.as_view(),name="request"),
    path("provider-offer/<int:id>/",provider_offer.as_view(),name="provideroffer"),
    path("provider-work/",provider_work.as_view(),name="providerwork"),

    path("select-role/",selectrole.as_view(),name="selectrole"),

    path("customer-detail/<int:booking_id>/",CustomerDetail.as_view(),name="detail"),


]