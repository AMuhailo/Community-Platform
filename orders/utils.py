import datetime 
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from orders.models import Order

class MemberBarrier(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_administrator:
            return redirect('booking_list_url')
        return super().dispatch(request, *args, **kwargs)
    
    
def order_completed(orders):
    now = timezone.now().date()
    for order in orders:
        trips_over = order.booking.end_time.date()
        if now >= trips_over + datetime.timedelta(days = 1):
            order.delete()
            return True
    return False 