import uuid
from django.db import models    
from django.contrib.auth.models import User
from admin_side.models import Product,Coupon
from django.conf import settings

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(max_length=250, null=True, blank=True)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone_1 = models.CharField( null=True, blank=True)
    phone_2 = models.CharField( null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Addresses"

    def _str_(self):
        return f"{self.full_name}'s Address"
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add this field for discounted price
    def __str__(self):
        return self.product.Product_Name
    
    def total_price(self):
        discounted_price = self.product.get_discounted_price()

        if discounted_price is not None:
            return discounted_price * self.quantity
        else:
            return self.product.price * self.quantity
    
    
  
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user', null=True,blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    billing_status = models.CharField(max_length=10,default=total_paid )
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    
    # New field for order status
    RETURNED ='returned'
    CANCEL = 'cancelled'
    ORDER_STATUS_CHOICES = [
        ('confirmed', 'Order Confirmed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled','cancelled'),
        ('returned','returned'),
        # Add more statuses as needed
    ]

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='confirmed')

    class Meta:
        ordering = ('-created',)

    def str(self):
        return f"{self.created} - {self.status}"

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def str(self):
        return str(self.id)

    class MaxValidator:
        pass
 
class Returnedproduct(models.Model):
    RETURN_PENDING = 'Return Pending'
    RETURNED = 'Returned'
    REJECTED = 'Rejected'

    RETURN_STATUS_CHOICES = (
        (RETURN_PENDING, 'Return Pending'),
        (RETURNED, 'Returned'),
        (REJECTED, 'Rejected')
    )

    order = models.ForeignKey(Order, related_name='returned_products', on_delete=models.CASCADE)
    reason = models.TextField()
    return_status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default=RETURN_PENDING)
    returned_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"{self.order.id} - {self.return_status}"
    
    
class Wallet(models.Model):
    DEBIT = 'Debit'
    CREDIT = 'Credit'

    BALANCE_TYPE = (
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit')
    )
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order =models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(default=0)
    balance_type = models.CharField(max_length=15, choices=BALANCE_TYPE, default=CREDIT)
    balance_returned = models.DateTimeField(auto_now_add=True)
    transaction_description = models.TextField(blank=True, null=True)
     
    def _str_(self):
        return f"{self.user.username}'s Wallet"

    def total_balance(self):
        balance = 0
        if self.balance_type == Wallet.DEBIT:
            balance -= self.amount
        else:
            balance += self.amount
        return balance
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    
    