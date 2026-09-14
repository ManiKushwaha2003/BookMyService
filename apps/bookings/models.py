from django.db import models

from apps.accounts.models import User, ProviderProfile
from apps.services.models import Service
from apps.core.models import TimeStampedMixing
# Create your models here.


class Booking(TimeStampedMixing):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("IN_PROGRESS","In_Progress"),
        ("REJECTED", "Rejected"),
        ("COMPLETED", "Completed")
    )

    client = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )


    service = models.ForeignKey(Service,
        on_delete=models.CASCADE,
        related_name="bookings")

    
    description = models.TextField(blank=True)

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,        
        related_name="bookings"
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    def __str__(self):
        return f"{self.client.username} - {self.service.name}"

class BookingOffer(TimeStampedMixing):
    STATUS_CHOICES = (
        ("PENDING","Pending"),
        ("ACCEPTED","Accepted"),
        ("REJECTED", "Rejected"),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="offers")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="offers")
    price = models.IntegerField()
    messages = models.TextField(blank=True)
    status = models.CharField( max_length=50, choices=STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return f"{self.provider.user.username} - {self.price}"

  