from random import randint
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from employees.forms import RegisterUserForm, ModeratorCreateForm
from employees.models import Administrator, User, Profile, Moderator

# Create your views here.

class RegisterUser(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        User.objects.update(is_administrator = False, is_member = True)
        return super().form_valid(form)
    
    
    
class ModeratorCreateView(CreateView):
    model = Moderator
    form_class = ModeratorCreateForm
    template_name = 'registration/moder_create.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        moder = form.save(commit = False)
        moder.is_administrator = False
        moder.is_member = False
        moder.set_password(str(randint(1000,10000)))
        moder.is_moder = True
        moder.save()
        admin = Administrator.objects.first()
        Moderator.objects.create(user = moder.profile, admin = admin)
        return super().form_valid(form)