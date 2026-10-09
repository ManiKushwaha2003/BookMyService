from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.bookings.models import Booking
from .models import Rating
from .serializers import RatingSerializer
from apps.accounts.models import ProviderProfile
from django.db.models import Avg, Count


class RatingAPIView(APIView):

    def post(self, request):

        booking = Booking.objects.get(
            id=request.data["booking"]
        )

        if booking.status != "COMPLETED":
            return Response(
                {"msg": "Service is not completed yet"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.provider is None:
            return Response(
                {"msg": "Provider is not selected"},
                status=status.HTTP_400_BAD_REQUEST
        )
        if Rating.objects.filter(booking=booking).exists():
            return Response(
                {"msg": "This booking has already been rated"},
                status=status.HTTP_400_BAD_REQUEST
            )


        rating = Rating.objects.create(
            client=booking.client,
            provider=booking.provider,
            booking=booking,
            rating=request.data["rating"],
            comment=request.data.get("comment", "")
        )

        serializer = RatingSerializer(rating)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


    def get(self, request):

        provider = ProviderProfile.objects.get(
            user=request.user
        )

        rating = Rating.objects.filter(
            provider=provider
        ).aggregate(
            average_rating=Avg("rating"),
            total_rating=Count("id")
        )
        average_rating = rating["average_rating"] or 0

        return Response({
            "average_rating": round(float(average_rating), 1),
            "total_rating": rating["total_rating"]
        })