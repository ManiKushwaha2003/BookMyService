from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import BookingOffer,Booking
from .serializers import BookingSerializer,BookingOfferSerializer
from apps.accounts.models import ProviderProfile


class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        booking = Booking.objects.filter(client=request.user)
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = BookingSerializer(data = request.data,)
        if serializer.is_valid():
            serializer.save(client=request.user)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class BookingByIdView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        booking = Booking.objects.get(id=id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self,request,id):
        booking = Booking.objects.get(id=id)
        serializer = BookingSerializer(booking, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self,request,id):
        booking = Booking.objects.get(id=id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookingOfferAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        offer = BookingOffer.objects.filter(booking__client=request.user)
        serializer = BookingOfferSerializer(offer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        booking_id = request.data.get("booking")
        provider_id = request.data.get("provider")

        booking = Booking.objects.get(id=booking_id)

        if booking.status != "PENDING":
            return Response({"msg":"this booking is accepted"}, status=status.HTTP_400_BAD_REQUEST)

        offer_exists=BookingOffer.objects.filter(booking_id=booking_id, provider_id=provider_id).exists()

        if offer_exists:
            return Response({"msg":"already send a offer"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingOfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingOfferById(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        offers = BookingOffer.objects.get(id=id)
        serializer = BookingOfferSerializer(offers)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def patch(self,request,id):
        offer = BookingOffer.objects.get(id=id)
        serializer = BookingOfferSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def delete(self,request,id):
        booking = BookingOffer.objects.get(id=id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      
             

class BookingoffersByBookingView(APIView):
    def get(self, request, booking_id):
        offers = BookingOffer.objects.filter(booking_id=booking_id)
        serializer = BookingOfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptOfferView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id):
        offer = BookingOffer.objects.get(id=id)

        booking = offer.booking

        if booking.status != "PENDING":
            return Response({"msg": "This booking is already accepted."}, status=status.HTTP_400_BAD_REQUEST)        

        booking.provider = offer.provider
        booking.status = "ACCEPTED"
        booking.save()

        offer.status = "ACCEPTED"
        offer.save()

        BookingOffer.objects.filter(booking=booking).exclude(id=offer.id).update(status="REJECTED")

        return Response({"msg":"Provider Selecled Succesfully"}, status=status.HTTP_200_OK)

class BookingCompleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, booking_id):

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"msg": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # If booking is already completed,
        # make sure accepted offer is also completed
        if booking.status == "COMPLETED":

            BookingOffer.objects.filter(
                booking=booking,
                status="ACCEPTED"
            ).update(
                status="COMPLETED"
            )

            return Response(
                {
                    "msg": "Booking is already completed",
                    "status": booking.status
                },
                status=status.HTTP_200_OK
            )

        # Booking must be accepted before completing
        if booking.status != "ACCEPTED":
            return Response(
                {"msg": "Booking is not accepted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update Booking
        booking.status = "COMPLETED"
        booking.save()

        # Update accepted BookingOffer
        BookingOffer.objects.filter(
            booking=booking,
            status="ACCEPTED"
        ).update(
            status="COMPLETED"
        )

        return Response(
            {
                "msg": "Booking completed successfully",
                "status": booking.status
            },
            status=status.HTTP_200_OK
        )