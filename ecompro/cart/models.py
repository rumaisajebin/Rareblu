from django.db import models    
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(max_length=250, null=True, blank=True)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone_1 = models.CharField(max_length=10, null=True, blank=True)
    phone_2 = models.CharField(max_length=10, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Addresses"

    def _str_(self):
        return f"{self.full_name}'s Address"
    