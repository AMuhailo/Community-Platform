from django import forms
from django.utils import timezone
from booking.models import Booking, Vehicle, Review

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
                'id':'from_place',
            }),
            'to_place':forms.TextInput(attrs = {
                'class':"form-control",
                'id':'to_place',
            }),
            'start_time':forms.DateInput(attrs = {
                'class':"form-control",
                'id':'start_time',
            }),
            'end_time':forms.DateInput(attrs = {
                'class':"form-control",
                'id':'arrival_time',
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
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']
        
        
class TripDeleteForm(forms.Form):
    delete = forms.BooleanField(initial = False)