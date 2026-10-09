from django.contrib import admin
from . models import User
from .models import ProviderProfile

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=["id","username","role", "email", "first_name", "last_name"]

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display=["id" ]
    
    
    

