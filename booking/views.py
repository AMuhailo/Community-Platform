from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView, CreateView
from django.db.models import Avg, Max, Min, Q
from django.contrib.auth import get_user_model
from flask import request
from booking.models import Vehicle, Booking
from booking.forms import BookingForm, VehicleForm

# Create your views here.
User = get_user_model()

class SuccessMixin:
    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs.update({
                'request':self.request
            })
            return kwargs
    def get_success_url(self):
        return reverse_lazy('profile_url', args = [self.request.user.username])



class BookingListView(ListView):
    model = Booking
    context_object_name = 'trips'
    template_name = 'page/booking/booking_list.html'
    def get_queryset(self):
        queryset = Booking.objects.annotate(time = Min('end_time') - Min('start_time')).all()
        self.date = self.request.GET.get('date')
        self.time = self.request.GET.get('time')
        self.from_place = self.request.GET.get('from_place')
        self.to_place = self.request.GET.get('to_place')
        self.transport = self.request.GET.get('transport')
        if self.date:
            queryset = queryset.filter(start_time__date__gte = self.date)
        if self.time:
            queryset = queryset.filter(start_time__time__gte = self.time)
        if self.from_place:
            queryset = queryset.filter(from_place = self.from_place)       
        if self.to_place:
            queryset = queryset.filter(to_place = self.to_place)       
        if self.transport:
            queryset = queryset.filter(vehicle__vehicle = self.transport)   
        return queryset


class BookingDetailView(DetailView):
    model = Booking
    context_object_name = 'trip'
    template_name = 'page/booking/booking_detail.html'
    
    def get_object(self, queryset = ...):
        queryset = Booking.objects.annotate(time = Min('end_time') - Min('start_time'))
        return get_object_or_404(queryset, id = self.kwargs.get('booking_number'))


class BookingCreateView(SuccessMixin, CreateView):
    model = Booking    
    form_class = BookingForm
    template_name = 'page/booking/booking_update.html'
    def form_valid(self, form):
        cd = form.cleaned_data
        new_booking = form.save(commit = False)
        new_booking.vehicle = cd['vehicle']
        
        new_booking.save()
        return super().form_valid(form)
    

class BookingUpdateView(SuccessMixin, UpdateView):
    model = Booking    
    form_class = BookingForm
    context_object_name = 'trip'
    template_name = 'page/booking/booking_update.html'
    def get_object(self, queryset = ...):
        queryset = Booking.objects.annotate(time = Min('end_time') - Min('start_time'))
        return get_object_or_404(queryset, id = self.kwargs.get('booking_number'))

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'page/vehicle/vehicle_list.html'
    context_object_name = 'vehicles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, self.request.user.username)
        return context
    
class VehicleCreateView(SuccessMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'page/vehicle/vehicle_update.html'
    
    def form_valid(self, form):
        new_vehicle = form.save(commit=False)
        new_vehicle.owner = self.request.user.profile.member_user   
        new_vehicle.save()
        return super().form_valid(form)

class VehicleUpdateView(SuccessMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'page/vehicle/vehicle_update.html'
    
    def get_object(self):
        return get_object_or_404(Vehicle, id = self.kwargs.get('vehicle_number'))