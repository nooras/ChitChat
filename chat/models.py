from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserId(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    uniqueId = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username}'

class MessageModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) # will be set only one time

    def __str__(self):
        return str(self.sender)

    class Meta:
        ordering = ["timestamp"]
