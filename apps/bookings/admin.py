from django.contrib import admin
from .models import Booking, BookingOffer
# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=["id","client","service","description","status"]

@admin.register(BookingOffer)
class BookingOfferAdmin(admin.ModelAdmin):
    list_display=["id","booking","provider","price","messages","status"]
    
  
    
