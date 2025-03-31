from re import A
from django import forms
from django.utils import timezone
from booking.models import Booking, Vehicle

class BookingForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(queryset = Vehicle.objects.none(), required=False, widget = forms.Select(attrs={"class":'form-select'}))
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
            'start_time':forms.TimeInput(attrs = {
                'class':"form-control",
            }),
            'end_time':forms.TimeInput(attrs = {
                'class':"form-control",
            }),
        }
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(owner = request.user.profile)
        
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ['owner']
        widgets = {
            'vehicle':forms.Select(attrs={
                "class":'form-control'}),
            'brand':forms.TextInput(attrs={
                "class":'form-control', 
                'placeholder':'Toyota, Audo, BMW....'}),
            'year':forms.TextInput(attrs={
                "class":'form-control', 
                'placeholder':'2017'}),
            'capacity':forms.NumberInput(attrs={
                "class":'form-control', 
                'placeholder':'Number of passenger seats'}),
            'location':forms.TextInput(attrs={
                "class":'form-control', 
                'placeholder':'Your city'}),
        }
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(owner = request.user.profile)
        
        