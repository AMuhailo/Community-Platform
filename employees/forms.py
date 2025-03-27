from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from employees.models import Moderator, Profile
User = get_user_model()

class RegisterUserForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.FileField(required = False)
    number = forms.CharField(max_length = 20, required = False)
    age = forms.IntegerField(initial = 18)
    bio = forms.CharField(widget = forms.Textarea, required=False)
    class Meta:
        model = User
        fields = ['avatar','first_name', 'last_name', 'email', 'number', 'age', 'bio']

        