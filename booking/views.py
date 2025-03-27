from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Avg, Max, Min
from booking.models import Vehicle, Booking

# Create your views here.

class BookingListView(ListView):
    model = Booking
    context_object_name = 'booking'
    template_name = 'page/vehicle/vehicle_list.html'
    queryset = Booking.objects.all().annotate(time = Min('end_time__time') - Min('start_time__time'))