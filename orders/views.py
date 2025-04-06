from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from booking.models import Booking, Vehicle
from orders.forms import OrderCreateForm, OrderDeleteForm
from orders.models import Order
from orders.tasks import order_create_task
from orders.utils import MemberBarrier, order_completed
# Create your views here.

class OrderMixin(LoginRequiredMixin):
    model = Order
    context_object_name = 'orders'
    def get_queryset(self):
        orders = Order.objects.filter(date__gte = timezone.now().date()).select_related('booking','user','owner','booking__vehicle')
        order_completed(orders)
        return orders
    
class OrderListView(OrderMixin, ListView):
    template_name = 'page/orders/orders_list.html'
    
    
class OrderAllListView(MemberBarrier, OrderMixin, ListView):
    template_name = 'page/orders/orders_allist.html'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'page/orders/orders_created.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('booking_list_url')
    def get_object(self, queryset = ...):
        return get_object_or_404(Booking, id = self.kwargs.get('booking_id')) 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trip"] = self.get_object()
        return context
        
    def form_valid(self, form):
        booking = self.get_object()
        user = self.request.user
        cd = form.cleaned_data
        booking.vehicle.capacity_order(cd['capacity'])
        orders = form.save(commit = False)
        orders.booking = booking
        orders.price = booking.price
        orders.user = user
        orders.owner = booking.vehicle.owner.user
        orders.save()
        if booking.vehicle.capicity == 0:
            booking.status = 'pending'
            booking.save()
        order_create_task.delay(orders.id, booking.id , user.id, cd['capacity'])
        return  super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
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
    