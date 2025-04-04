import datetime 
from django.utils import timezone
from orders.models import Order


def order_completed(orders):
    now = timezone.now().date()
    for order in orders:
        trips_over = order.booking.end_time.date()
        if now >= trips_over + datetime.timedelta(days = 1):
            order.delete()
            return True
    return False 