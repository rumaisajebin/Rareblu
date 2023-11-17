from django.db import models
from django.contrib.auth.models import User,auth



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
    img1 = models.ImageField(upload_to='product')
    img2 = models.ImageField(upload_to='product')
    img3 = models.ImageField(upload_to='product')
    img4 = models.ImageField(upload_to='product')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.Product_Name
    
    

class Order(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    pincode=models.CharField(max_length=6)
    city=models.CharField(max_length=200)
    paid_amount=models.IntegerField(default=0)
    is_paid=models.BooleanField(default=False)
    mercahant_id=models.CharField(max_length=255)
    created_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='orders')
    created_at=models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,related_name='items',on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    
 