from django import forms
from django.utils import timezone
from booking.models import Booking, Vehicle

class BookingForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(queryset = Vehicle.objects.none(), widget = forms.Select(attrs={"class":'form-select'}))
    brand = forms.CharField(max_length = 120, required = False, widget = forms.TextInput(attrs={"class":'form-control', 'placeholder':'Toyota, Audo, BMW....'}))
    year = forms.IntegerField(required = False, widget = forms.TextInput(attrs={"class":'form-control', 'placeholder':'20017'}))
    capacity = forms.IntegerField(required = False, widget = forms.NumberInput(attrs={"class":'form-control', 'placeholder':'Number of passenger seats'}))
    class Meta:
        model = Booking
        fields = ['price','from_place','to_place','start_time','end_time']
        widgets = {
            'price':forms.NumberInput(attrs = {
                'class':"form-control",
                'id':"price-label"
            }),
            'from_place':forms.TextInput(attrs = {
                'class':"form-control",
            }),
            'to_place':forms.TextInput(attrs = {
                'class':"form-control",
            }),
            'start_time':forms.TextInput(attrs = {
                'class':"form-control",
            }),
            'end_time':forms.TextInput(attrs = {
                'class':"form-control",
            }),
        }
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(owner = request.user.profile.member_user)