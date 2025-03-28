import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from employees.models import Member
# Create your models here.

User = get_user_model()

class Vehicle(models.Model):
    VEHICLE_CHOICES = [
        ('car', "Car"),
        ('bus', "Bus"),
    ]
    vehicle = models.CharField(max_length = 3, choices = VEHICLE_CHOICES , default = 'bus')
    brand = models.CharField(max_length = 120)
    year = models.PositiveSmallIntegerField(default = timezone.now().year)
    capicity = models.PositiveSmallIntegerField(default = 2)
    location = models.CharField(max_length = 120, blank = True, null = True)
    owner = models.ForeignKey(Member, on_delete = models.CASCADE, related_name = 'owner_vehicle')
    
    class Meta:
        ordering = ['-year']
    
    def __str__(self):
        return f"{self.vehicle} {self.brand}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), 
        ('confirmed', 'Confirmed'), 
        ('cancelled', 'Cancelled')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete = models.CASCADE, related_name = 'vehicle_booking')
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    from_place = models.CharField(max_length = 120)
    to_place = models.CharField(max_length = 120)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, blank = True, null = True)

    class Meta:
        ordering = ['-id','-start_time','end_time']
        indexes = [models.Index(fields = ['start_time']),
                   models.Index(fields = ['-end_time'])]
    
    def get_absolute_url(self):
        return reverse("booking_detail_url", args = [self.id])
    
    
    def __str__(self):
        return f"Booking №{self.id}"