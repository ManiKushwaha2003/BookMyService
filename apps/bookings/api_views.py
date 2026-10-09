from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import BookingOffer,Booking
from .serializers import BookingSerializer,BookingOfferSerializer
from apps.accounts.models import ProviderProfile


class BookingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):   
        print("request user :", request.user.id)
        print("Role inside booking :", request.user.role)
        if request.user.is_superuser:
            booking = Booking.objects.all()
        else:
            booking = Booking.objects.filter(client=request.user)

        search = request.query_params.get("search")
   
        booking_status = request.query_params.get("status")

        if booking_status:
            booking = booking.filter(status=booking_status)

        if search:
            booking = booking.filter(
                Q(service__name__icontains=search) |
                Q(provider__user__username__icontains=search)
            )

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
        if request.user.is_superuser:
            offer = BookingOffer.objects.all()
        else:
            offer = BookingOffer.objects.filter(booking__client=request.user)
        serializer = BookingOfferSerializer(offer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):

        booking_id = request.data.get("booking")
        booking = Booking.objects.get(id=booking_id)

        if booking.status != "PENDING":
            return Response(
                {"msg":"this booking is accepted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        provider = ProviderProfile.objects.get(user=request.user)

        offer_exists = BookingOffer.objects.filter(
            booking_id=booking_id,
            provider=provider
        ).exists()

        if offer_exists:
            return Response(
                {"msg":"already send a offer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BookingOfferSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(provider=provider)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

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
class BookingProviderPendingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        provider = ProviderProfile.objects.get(user=request.user)
        bookings = Booking.objects.filter(
            service__in=provider.services.all(),
            status="PENDING"
        )

        serializer = BookingSerializer(bookings, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )    

class ProviderWorkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        provider = ProviderProfile.objects.get(
            user=request.user
        )

        offers = BookingOffer.objects.filter(
            provider=provider,status="COMPLETED"
        )


        search = request.query_params.get("search","").strip()
        booking_status = request.query_params.get("status","").strip()

        if booking_status:
            offers = offers.filter(status=booking_status)

        if search:
            offers = offers.filter(
                Q(booking__client__username__icontains=search) |
                Q(booking__service__name__icontains=search)
            )  

        serializer = BookingOfferSerializer(
            offers,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )    
