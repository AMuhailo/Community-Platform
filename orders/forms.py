from django import forms
from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['capacity']
        
        
class OrderDeleteForm(forms.Form):
    deleted = forms.BooleanField(initial = False)
