from django.db import models
import uuid

from booking.models import Booking, User
# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    booking = models.ForeignKey(Booking, on_delete = models.CASCADE, related_name = 'order_booking')
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    capacity = models.PositiveSmallIntegerField(default = 1)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'order_user')
    
    def __str__(self):
        return f"Order №{self.id}"