from django.urls import path

from .api_views import BookingAPIView, BookingByIdView, BookingOfferAPIView, BookingOfferById, AcceptOfferView, BookingoffersByBookingView, BookingCompleteAPIView, BookingProviderPendingView, ProviderWorkAPIView

urlpatterns = [
    
    path("booking/", BookingAPIView.as_view(), name="booking"),
    path("booking/<int:id>", BookingByIdView.as_view(), name="booking_by_id"),

    path("booking/offer/", BookingOfferAPIView.as_view(), name="offer"),
    path("booking/offer/<int:id>",BookingOfferById.as_view(), name="offer_by_id"), 

    path("booking/<int:booking_id>/offers/", BookingoffersByBookingView.as_view(),name="booking_offers"),
    path("booking/offer/accept/<int:id>", AcceptOfferView.as_view(), name="accept"),

    path("booking/<int:booking_id>/complete/", BookingCompleteAPIView.as_view()),
    path("booking/provider/pending/", BookingProviderPendingView.as_view()),
    path("provider/work/", ProviderWorkAPIView.as_view()),

]
