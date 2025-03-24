from django.contrib import admin
from chat.models import GroupMessage, ChatGroup
# Register your models here.

admin.site.register(ChatGroup)
admin.site.register(GroupMessage)