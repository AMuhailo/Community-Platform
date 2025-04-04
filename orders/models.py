from django.db import models
from django.utils import timezone
import uuid

from booking.models import Booking, User
# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    booking = models.ForeignKey(Booking, on_delete = models.CASCADE, related_name = 'order_booking')
    price = models.DecimalField(max_digits = 10, decimal_places = 2 , null = True)
    capacity = models.PositiveSmallIntegerField(default = 1)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'order_owner')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'order_user')
    date = models.DateField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields = ['-created']),
                   models.Index(fields = ['id'])]
        
    def __str__(self):
        return f"Order №{str(self.id)[:4]}"