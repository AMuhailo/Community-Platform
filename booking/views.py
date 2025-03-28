from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView, CreateView
from django.db.models import Avg, Max, Min
from booking.models import Vehicle, Booking
from booking.forms import BookingForm

# Create your views here.

class BookingListView(ListView):
    model = Booking
    context_object_name = 'trips'
    template_name = 'page/vehicle/booking_list.html'
    queryset = Booking.objects.all().annotate(time = Min('end_time') - Min('start_time'))
    

class BookingDetailView(DetailView):
    model = Booking
    context_object_name = 'trip'
    template_name = 'page/vehicle/booking_detail.html'
    
    def get_object(self, queryset = ...):
        queryset = Booking.objects.annotate(time = Min('end_tim') - Min('start_time'))
        return get_object_or_404(queryset, id = self.kwargs.get('booking_number'))


class BookingCreateView(CreateView):
    model = Booking    
    form_class = BookingForm
    template_name = 'page/vehicle/booking_update.html'
    def form_valid(self, form):
        cd = form.cleaned_data
        new_booking = form.save(commit = False)
        if not self.request.user.profile.member_user.owner_vehicle.get(owner=self.request.user.profile.member_user):
            vehicle = Vehicle.objects.create(brand = cd['brand'], year = cd['year'], capicity = cd['capacity'],owner = self.request.user.profile.member_user)
            vehicle.save()
            new_booking.vehicle = vehicle
        else:
            new_booking.vehicle = cd['vehicle']
        
        new_booking.save()
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request':self.request
        })
        return kwargs
    def get_success_url(self):
        return reverse('profile_url', args = [self.request.user.username])
    

class BookingUpdateView(UpdateView):
    model = Booking    
    form_class = BookingForm
    context_object_name = 'trip'
    template_name = 'page/vehicle/booking_update.html'
    def get_object(self, queryset = ...):
        queryset = Booking.objects.annotate(time = Min('end_time') - Min('start_time'))
        return get_object_or_404(queryset, id = self.kwargs.get('booking_number'))
    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs.update({
                'request':self.request
            })
            return kwargs
    def get_success_url(self):
        return reverse_lazy('profile_url', args = [self.request.user.username])