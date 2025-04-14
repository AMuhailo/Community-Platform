import requests
import plotly.express as pl
from random import choice, randint
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, FormView, TemplateView
from booking.models import Review
from employees.forms import CategoryUpdateForm, RegisterUserForm, UserCreateForm, ProfileUpdateForm
from employees.models import Administrator, Profile, Moderator, Member
from employees.tasks import category_task
from orders.utils import MemberBarrier, order_completed
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
    
    
class ProfileUser(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'employees/profile.html'
    
    def get_object(self, queryset = ...):
        return get_object_or_404(self.model, username = self.kwargs.get('username'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["vehicles"] = []
        context['moders'] = []
        if self.request.user.is_administrator:
            queryset = self.get_object().administrator.filter(user__username=user.username).first()      
            if queryset:
                context['moders'] = queryset.moderator_admin.all().select_related('user','user__user')
        if self.request.user.is_member:
            orders = user.order_user.filter(user = user)
            order_completed(orders)
            context['orders'] = orders
        if hasattr(user, 'profile') and (hasattr(user.profile, 'member_user') or hasattr(user.profile,'moder_user')):
            if user.profile.member_user.category == 'DR':
                context["vehicles"] = user.profile.owner_vehicle.all().select_related('owner','owner__user','owner__moderator_user__user__user__profile','owner__member_user__user')
        return context

    
class ModeratorCreateView(MemberBarrier, LoginRequiredMixin, CreateView):
    model = Moderator
    form_class = UserCreateForm
    template_name = 'employees/moder/moder_create.html'
    success_url = reverse_lazy('booking_list_url')
    
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
    
class ModeratorListView(MemberBarrier, LoginRequiredMixin, ListView):
    model = Moderator
    template_name = 'employees/moder/moder_list.html'
    context_object_name = 'moderators'
    queryset = Moderator.objects.filter(user__user__is_moder = True)
    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'employees/profile_update.html'
    context_object_name = 'user'
    form_class = ProfileUpdateForm
    
    def get_object(self, queryset = ...):
        return get_object_or_404(User, username = self.kwargs.get('username'), id = self.kwargs.get('user_id'))

    def get_success_url(self):
        return reverse("profile_url", args = [self.request.user.username])
    
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


class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    context_object_name = 'members'
    template_name = 'employees/member/member_list.html'
    queryset = Member.objects.filter(user__user__is_member = True).select_related('user','user__user')
    

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    template_name = 'employees/profile_update.html'
    context_object_name = 'category'
    form_class = CategoryUpdateForm
    
    def get_object(self, queryset = ...):
        return get_object_or_404(Member, id = self.kwargs.get('member_id'))
    
    def get_success_url(self):
        return reverse("profile_url", args = [self.request.user.username])


def change_category(request, user_pk):
    user = User.objects.get(id = user_pk)
    
    profile = request.user.profile
    category_task.delay(user.id, profile.id)
    return redirect('profile_url', request.user.username)

def char_review_member(request):
    response = requests.get(settings.CHAR_API)
    
    if response.status_code == 200:
        data = response.json()
        users_data = [user['user'] for user in data['member']]
        reviews = [review['review'] for review in data['member']]
        
        fig = pl.bar(x = users_data , y = reviews, title = 'User review', labels={"x":"User Name", 'y':"Reviews"})
        char = fig.to_html()
    users = User.objects.all()[:6]
    context = {"char":char, 'users':users, 'user':request.user}
    return render(request, 'employees/moder/char.html',context)