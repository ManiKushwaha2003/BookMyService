from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.services.models import Service
# Create your models here.

class User(AbstractUser):
     
    ROLE_CHOICES=(
        ("admin","Admin"),
        ("provider","Provider"),
        ("user","User"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

class ProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider_profile"
    )
    services = models.ManyToManyField(Service)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)