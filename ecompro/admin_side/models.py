from datetime import timezone
from django.db import models
from django.contrib.auth.models import User,auth
from django.db import models
from image_cropping import ImageRatioField


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name=models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    Product_Name = models.CharField(max_length=100, default='DefaultProductName')
    Brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
    Category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    Stock = models.IntegerField(default=0)
    Description = models.CharField(max_length=100, default='Default Description')
    img1 = models.ImageField(upload_to='product',blank=True)
    img2 = models.ImageField(upload_to='product',blank=True)
    img3 = models.ImageField(upload_to='product',blank=True)
    img4 = models.ImageField(upload_to='product',blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.Product_Name

    
class Coupon(models.Model):
    coupon_code=models.CharField(max_length=10)
    is_expired=models.DateField()
    discount_price=models.IntegerField(default=100)
    minimum_amount=models.IntegerField(default=500)
    active =models.BooleanField(default=True)
    
    def __str__(self):
        return self.coupon_code
    
    def is_expired(self):
        return self.expiry_date < timezone.now().date()
  


 