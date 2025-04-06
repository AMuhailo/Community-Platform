from django import forms
from booking.models import Vehicle
from orders.models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['capacity']

        
class OrderDeleteForm(forms.Form):
    deleted = forms.BooleanField(initial = False)
