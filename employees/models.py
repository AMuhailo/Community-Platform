from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_administrator = models.BooleanField(default = True)
    is_moder = models.BooleanField(default = False)
    is_member = models.BooleanField(default = False)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')
    avatar = models.FileField(upload_to = 'avatar/', blank = True, null = True)
    number = models.CharField(max_length = 20, blank = True, null = True)
    age = models.IntegerField(default = 0)
    
    class Meta:
        ordering = ['user']
        indexes = [models.Index(fields = ['-user']),
                   models.Index(fields = ['-id'])]
    
    def __str__(self):
        return self.user.get_full_name()
    
class Administrator(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'administrator')

    def __str__(self):
        return self.user.username
    
    
class Moderator(models.Model):
    user = models.OneToOneField(Profile, on_delete = models.CASCADE, related_name = 'moderator_user')
    admin = models.ForeignKey(Administrator, on_delete = models.CASCADE, related_name = 'moderator_admin')
    
    def __str__(self):
        return self.user.user.get_full_name()

class Member(models.Model):
    user = models.OneToOneField(Profile, on_delete = models.CASCADE, related_name = 'member_user')

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return self.user.user.get_full_name()