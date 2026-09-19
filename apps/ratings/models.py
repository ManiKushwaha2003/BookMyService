from django.db import models
from apps.accounts.models import User,ProviderProfile
from apps.bookings.models import Booking
from apps.core.models import TimeStampedMixing


# Create your models here.
class Rating(models.Model):

    client = models.ForeignKey(User, on_delete=models.CASCADE,related_name="rating")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="rating")
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="rating")
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.provider.user.username} - {self.rating}"