from django.db import models
from django.contrib.auth.models import User,auth
from django.db import models


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CategoryOffer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    percent_offer = models.DecimalField(max_digits=5, decimal_places=2)  # Example: 10.00 for 10%
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    
    def __str__(self):
        return f"Offer for {self.category.name} - {self.percent_offer}%"

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
    d_price = models.IntegerField(default=0)
    Stock = models.IntegerField(default=0)
    Description = models.CharField(max_length=100, default='Default Description')
    img1 = models.ImageField(upload_to='product',blank=True)
    img2 = models.ImageField(upload_to='product',null=True,default=None)
    img3 = models.ImageField(upload_to='product',null=True,default=None)
    img4 = models.ImageField(upload_to='product',null=True,default=None)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.Product_Name
    
    
class Coupon(models.Model):
    coupon_code=models.CharField(max_length=100,unique=True)
    is_expired=  models.DateField(null=True)
    discount_price=models.IntegerField(default=100)
    minimum_amount=models.IntegerField(default=500)
    active =models.BooleanField(default=True)
    
    def __str__(self):
        return self.coupon_code


class Applied_coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    coupon = models.CharField(max_length=50, null=True, blank=True)
    applied = models.BooleanField(default=True)
 