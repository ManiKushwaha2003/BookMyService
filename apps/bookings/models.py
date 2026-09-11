
from django.db import models
from apps.accounts.models import User, ProviderProfile
from apps.services.models import Service
from apps.core.models import TimeStampedMixing
# Create your models here.


class Booking(TimeStampedMixing):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
        ("COMPLETED", "Completed")
    )

    client = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    price=models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    def __str__(self):
        return f"{self.member.username} - {self.service.name}"