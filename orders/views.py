from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.core.mail import send_mail
from flask import redirect
from booking.models import Booking, Vehicle
from orders.forms import OrderCreateForm, OrderDeleteForm
from orders.models import Order

# Create your views here.

class OrderListView(ListView):
    model = Order
    template_name = 'page/orders/orders_list.html'
    context_object_name = 'orders'
    queryset = Order.objects.filter(date__gte = timezone.now().date())
    
class OrderCreateView(CreateView):
    model = Order
    template_name = 'page/orders/orders_created.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('booking_list_url')
    
    def get_object(self, queryset = ...):
        return get_object_or_404(Booking, id = self.kwargs.get('booking_id'))
    def form_valid(self, form):
        user = self.request.user
        cd = form.cleaned_data
        self.get_object().vehicle.capacity_order(cd['capacity'])
        orders = form.save(commit = False)
        orders.booking = self.get_object()
        orders.price = self.get_object().price
        orders.user = user
        orders.owner = self.get_object().vehicle.owner.user
        orders.save()
        subject = f"Your orders №{str(orders.id)[:-4]}"
        messages_user = f"You have placed an order for a car for on date {self.get_object().start_time} to your destination {self.get_object().to_place}"
        messages_owner = f"{self.get_object().vehicle.owner} decided to go on your route with number of seats {cd['capacity']} "
        send_mail(subject, messages_user, 'booking@gmail.com', [user.email])
        send_mail(subject, messages_owner, user.email, [self.get_object().vehicle.owner.user.email])
        return super().form_valid(form)
    

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'page/orders/orders_delete.html'
    form_class = OrderDeleteForm
    success_url = reverse_lazy('booking_list_url')
    def get_object(self, queryset = ...):
        return get_object_or_404(Order, id = self.kwargs.get('order_id'))
    def form_valid(self, form):
        cd = form.cleaned_data['deleted']
        if cd:
            order = self.get_object()
            email_owner = order.booking.vehicle.owner.user
            order.booking.vehicle.capacity_plus(order.capacity)
            subject = f'Order cancellation №{str(order.id)[:-4]}'
            message = f"Your order was canceled by the car owner"
            send_mail(subject, message, email_owner.email, [order.user])
            order.delete()
        else:
            return redirect('booking_list_url')
        return super().form_valid(form)
    