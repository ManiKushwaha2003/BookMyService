
from django.db import models
from apps.accounts.models import User, ProviderProfile
from apps.services.models import Service
# Create your models here.


class Booking(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.member.username} - {self.service.name}"