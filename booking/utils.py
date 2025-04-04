import datetime 
from django.utils import timezone
from booking.models import Booking, Vehicle

def trips_over(booking_ids):
    bookings =  Booking.objects.filter(id__in = booking_ids)
    now = timezone.now().date()
    for booking in bookings:
        if now >= booking.end_time.date() + datetime.timedelta(days=3) :
            booking.delete()
            return True
        else:
            print(f'I couldn`t delete this trips №'\
                f"{str(booking.id)[:4]}\n")
