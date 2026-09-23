from django.shortcuts import render
from django.urls import path

from apps.accounts.views import home, login, register, userdashboard, providerdashboard, createbooking, profile, booking_offers, my_booking, rating

# Create your views here.

ACCOUNTS_PREFIX = "accounts"

urlpatterns = [
    path("", home.as_view(),name="home"),
    path(f"{ACCOUNTS_PREFIX}/user/login/", login.as_view(), name="login"),
    path(f"{ACCOUNTS_PREFIX}/user/register/", register.as_view(), name="register"),
    path("user-dashboard/", userdashboard.as_view(), name="user_dashboard"),
    path("provider-dashboard/", providerdashboard.as_view(), name="user_dashboard"),
    path("create-booking/", createbooking.as_view(), name="create"),
    path("profile/", profile.as_view(),name="profile"),
    path("booking_offers/",booking_offers.as_view(),name="bookingoffers"),
    path("my_booking/",my_booking.as_view(),name="mybooking"),
    path("rating/<int:id>/",rating.as_view(),name="rating"),



]