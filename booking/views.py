from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView, CreateView
from django.db.models import Avg, Min, F, Count
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone
from booking.models import Review, Vehicle, Booking
from booking.forms import BookingForm, VehicleForm, ReviewForm

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
        queryset = Booking.objects.annotate(time = F('end_time') - F('start_time'), 
                                            average_rating=Avg('vehicle__owner__user__profile__user__review_received__rating'), 
                                            review_count=Count('vehicle__owner__user__profile__user__review_received'))\
                                            .filter(end_time__date__gte=timezone.now().date(),end_time__time__lte=timezone.now().time(), status='complete')\
                                            .select_related('vehicle',
                                                            'vehicle__owner',
                                                            'vehicle__owner__user',
                                                            'vehicle__owner__user__profile')
        Booking.objects.filter(end_time__date__lte=timezone.now().date(), end_time__time__lte=timezone.now().time()).update(status = 'cancelled')
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
        queryset = Booking.objects.annotate(time = F('end_time') - F('start_time'), 
                                            average_rating=Avg('vehicle__owner__user__profile__user__review_received__rating'), 
                                            review_count=Count('vehicle__owner__user__profile__user__review_received'))\
                                            .filter(status = 'complete')\
                                            .select_related('vehicle',
                                                            'vehicle__owner',
                                                            'vehicle__owner__user',
                                                            'vehicle__owner__user__profile')
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
    queryset = Vehicle.objects.all().select_related('user','user__profile','user__profile__member_user')
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
        new_vehicle.owner = self.request.user.profile
        new_vehicle.save()
        return super().form_valid(form)

class VehicleUpdateView(SuccessMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'page/vehicle/vehicle_update.html'
    
    def get_object(self):
        return get_object_or_404(Vehicle, id = self.kwargs.get('vehicle_number'))
    
class ReviewCreateView(CreateView):
    model = Review
    context_object_name = 'review'
    template_name = 'employees/profile_update.html'
    form_class = ReviewForm
    def get_success_url(self):
        return reverse("profile_url", args = [self.request.user.username])
    def form_valid(self, form):
        user = get_object_or_404(User, id=self.kwargs.get('user_pk'))
        review = form.save(commit=False)
        review.user = user
        review.reviewer = self.request.user
        review.save()
        return super().form_valid(form)