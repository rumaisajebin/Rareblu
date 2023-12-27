from django.db import models
from django.contrib.auth.models import User 
from .models import *
# Create your models here.

class Referral(models.Model):
    referal_code=models.CharField(max_length=100,blank=True)
    def __str__(self) :
        return self.referal_code

    @staticmethod
    def generate_referral_code(email, user_id):
        return f"rareblu-{email}-{user_id}rj"
    
class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile',null=True,default=None)
    address = models.CharField(max_length=100, blank=True)
    PhoneNumber = models.CharField(max_length=10, blank=True)
    referral = models.OneToOneField(Referral, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) :
        return self.user.username
