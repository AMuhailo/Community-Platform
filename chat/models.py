from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class ChatGroup(models.Model):
    name = models.CharField(max_length = 120, unique = True)
    
    def __str__(self):
        return self.name
    
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete = models.CASCADE, related_name = 'chat_messages')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'author_message')
    body = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
    
    def __str__(self):
        return f"{self.author}: {self.body[:30]}"

