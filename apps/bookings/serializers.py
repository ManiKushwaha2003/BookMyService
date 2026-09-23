from rest_framework import serializers
from django.db.models import Avg
from apps.ratings.models import Rating


from .models import Booking, BookingOffer

class BookingSerializer(serializers.ModelSerializer):  
    client_name = serializers.CharField(
        source="client.username",
        read_only=True
    )    

    service_name = serializers.CharField(
        source="service.name",
        read_only=True
    )

    provider_name = serializers.CharField(
        source="provider.user.username",
        read_only=True
    )      
   
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["client"]

class BookingOfferSerializer(serializers.ModelSerializer):

    provider_name = serializers.CharField(
        source="provider.user.username",
        read_only=True
    )

    service_name = serializers.CharField(
        source="booking.service.name",
        read_only=True
    )    
    provider_rating = serializers.SerializerMethodField()
    class Meta:
        model = BookingOffer
        fields = "__all__"  

    def get_provider_rating(self, obj):
        rating = obj.provider.rating.aggregate(average=Avg("rating"))
        return rating["average"] 
    

