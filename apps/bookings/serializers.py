from rest_framework import serializers
from django.db.models import Avg

from .models import Booking, BookingOffer

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class BookingOfferSerializer(serializers.ModelSerializer):
    provider_rating = serializers.SerializerMethodField()
    class Meta:
        model = BookingOffer
        fields = "__all__"  

    def get_provider_rating(self, obj):
        rating = obj.provider.rating.aggregate(average=Avg("rating"))
        return rating["average"]   