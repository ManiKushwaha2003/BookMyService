from django.db import models
from apps.core.models import TimeStampedMixing


# Create your models here

class Service(TimeStampedMixing):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
