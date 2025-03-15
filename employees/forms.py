from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from employees.models import Moderator
User = get_user_model()
class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
    
class ModeratorCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']