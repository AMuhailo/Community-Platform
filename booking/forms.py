from django import forms
from django.utils import timezone
from booking.models import Booking, Vehicle

class BookingForm(forms.ModelForm):
    brand = forms.CharField(max_length = 120)
    year = forms.IntegerField(initial = timezone.now().year)
    capacity = forms.IntegerField(initial = 2)
    class Meta:
        model = Booking
        fields = ['price','from_place','to_place','start_time','end_time']
        