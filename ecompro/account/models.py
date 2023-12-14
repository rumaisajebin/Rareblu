from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile',null=True,default=None)
    address = models.CharField(max_length=100, blank=True)
    PhoneNumber = models.CharField(max_length=10, blank=True)
    
    def __str__(self) :
        return self.user.username