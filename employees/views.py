from random import randint
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, FormView, TemplateView
from employees.forms import RegisterUserForm, UserCreateForm, ModeratorUpdateView
from employees.models import Administrator, Profile, Moderator, Member

# Create your views here.
User = get_user_model()

class RegisterUser(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_administrator = False
        user.is_member = True
        user.save()
        return super().form_valid(form)
    
class ModeratorCreateView(CreateView):
    model = Moderator
    form_class = UserCreateForm
    template_name = 'employees/moder/moder_create.html'
    success_url = reverse_lazy('moder_url')
    
    def form_valid(self, form):
        user = self.request.user
        moder = form.save(commit = False)
        moder.is_administrator = False
        moder.is_member = False
        moder.set_password(str(randint(1000,10000)))
        moder.is_moder = True
        moder.save()
        Moderator.objects.create(user = moder.profile, admin = user.administrator.get(user=user))
        return super().form_valid(form)
    
class ModeratorListView(ListView):
    model = Moderator
    template_name = 'employees/moder/moder_list.html'
    context_object_name = 'moderators'
    queryset = Moderator.objects.filter(user__user__is_moder = True)
    

class ModeratorUpdateView(UpdateView):
    model = User
    template_name = 'employees/moder/moder_update.html'
    context_object_name = 'moder'
    form_class = ModeratorUpdateView
    success_url = reverse_lazy("moder_url")
    
    def get_object(self, queryset = ...):
        return get_object_or_404(User, username = self.kwargs.get('username'), id = self.kwargs.get('user_id'))

    def get_initial(self):
        initial = super().get_initial()
        user = self.get_object()
        profile = Profile.objects.get(user = user)
        initial.update({
            'avatar':profile.avatar,
            'number':profile.number,
            'age':profile.age,
            'bio':profile.bio
        })
        return initial

    def form_valid(self, form):
        user = form.save(commit = False)
        user.save()
        profile = user.profile
        if form.cleaned_data['avatar']:
            profile.avatar = form.cleaned_data['avatar']
        profile.number = form.cleaned_data['number']
        profile.age = form.cleaned_data['age']
        profile.bio = form.cleaned_data['bio']
        profile.save()
        return super().form_valid(form)


class MemberListView(ListView):
    model = Member
    context_object_name = 'members'
    template_name = 'employees/member/member_list.html'
    queryset = Member.objects.filter(user__user__is_member = True)
