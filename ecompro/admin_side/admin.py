from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Coupon)
admin.site.register(Applied_coupon)