from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView, CreateView
from django.db.models import Avg, Max, Min
from booking.models import Vehicle, Booking
from booking.forms import BookingForm

# Create your views here.

class BookingListView(ListView):
    model = Booking
    context_object_name = 'trips'
    template_name = 'page/vehicle/booking_list.html'
    queryset = Booking.objects.all().annotate(time = Min('end_time__time') - Min('start_time__time'))
    

class BookingDetailView(DetailView):
    model = Booking
    context_object_name = 'trip'
    template_name = 'page/vehicle/booking_detail.html'
    
    def get_object(self, queryset = ...):
        queryset = Booking.objects.annotate(time = Min('end_time__time') - Min('start_time__time'))
        return get_object_or_404(queryset, id = self.kwargs.get('booking_number'))


class BookingCreateView(CreateView):
    model = Booking    
    form_class = BookingForm
    template_name = 'page/vehicle/booking_update.html'
    
    def get_success_url(self):
        return reverse_lazy('profile_url', args = [self.request.user.username])
    

class BookingUpdateView(UpdateView):
    model = Booking    
    form_class = BookingForm
    context_object_name = 'trip'
    template_name = 'page/vehicle/booking_update.html'
    def get_object(self, queryset = ...):
        queryset = Booking.objects.annotate(time = Min('end_time__time') - Min('start_time__time'))
        return get_object_or_404(queryset, id = self.kwargs.get('booking_number'))

    def get_success_url(self):
        return reverse_lazy('profile_url', args = [self.request.user.username])