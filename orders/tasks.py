from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from booking.models import Booking
from orders.models import Order
User = get_user_model()
@shared_task
def order_create_task(orders_id, booking_id, user_id, capacity = None):
    orders = Order.objects.get(id = orders_id)
    booking = Booking.objects.get(id = booking_id)
    user = User.objects.get(id = user_id)
    subject = f"Your orders №{str(orders.id)[:4]}"
    messages_user = f"You have placed an order for a car for on date {booking.start_time} to your destination {booking.to_place}"
    messages_owner = f"{booking.vehicle.owner} decided to go on your route with number of seats {capacity}.\nPhone - {user.profile.number}\Email - {user.email}"
    send_mail(subject, messages_user, 'booking@gmail.com', [user.email])
    send_mail(subject, messages_owner, user.email, [booking.vehicle.owner.user.email])