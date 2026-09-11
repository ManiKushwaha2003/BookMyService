from django.db import models
from apps.accounts.models import User,ProviderProfile
from apps.bookings.models import Booking
from apps.core.models import TimeStampedMixing


# Create your models here.
class Rating(models.Model):

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)