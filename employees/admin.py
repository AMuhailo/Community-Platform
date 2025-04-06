from django.contrib import admin
from employees.models import User, Profile, Administrator, Moderator, Member
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','avatar','number','age']


admin.site.register(Administrator)

@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = ['user','admin']
    
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user','category','created','updated']
    
