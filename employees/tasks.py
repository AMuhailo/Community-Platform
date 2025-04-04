from celery import shared_task
from random import choice
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse
from booking.models import Booking
from employees.models import User, Member, Moderator, Administrator, Profile


@shared_task
def category_task(user_id, profile_id):
    moders = Moderator.objects.values_list('user', flat = True)
    if moders:
        moder = User.objects.filter(id__in = moders)
        if not moder.exists():
            return "Not moder founded"
        else:
            email_moder = choice(moder)   
    user = User.objects.get(id = user_id)
    profile = Profile.objects.get(id = profile_id)
    subject = f"Change status"
    messages = f"User {user.get_full_name()} wants to change status. "\
                f"My status {profile.member_user.category}\n"
    return send_mail(subject, messages , user.email, [email_moder.email])