from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from employees.models import Profile, Member
User = get_user_model()

@receiver(post_save, sender = User)
def profile_post_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        
@receiver(post_save, sender = Profile)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user = instance)