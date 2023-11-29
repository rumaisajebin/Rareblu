from asyncio import exceptions
from datetime import timezone
import datetime
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect,get_list_or_404
from admin_side.models import Product, Category, Brand ,Coupon
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from cart.models import *
# Create your views here..



def admin_home(request):
    return render(request,'admin/admin_dashboard.html',{'title':'Dashboard'})



def category(request):
    cat = Category.objects.all()
    return render(request,'admin/admin_category.html', {'title':'Categories','cat': cat})


def categoryactive(request,id):
    category=Category.objects.get(id=id)
    
    if category.active:
        category.active=False
    else:
        category.active=True
    category.save()
    return redirect('category')


def editcategory(request,id):
    category = Category.objects.get(id=id)
    return render(request,'admin/edit_category.html',{'category':category})


def editcategory_action(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('editcategory')
        existing_category = Category.objects.filter(name = name)
        if existing_category.exists():
            messages.error(request,'category already exists')
            return redirect('editcategory')
        else:
            category = Category.objects.get(id=id)
            category.name = name
            category.save()
            return redirect ('category')


def addcategory(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        Category.objects.create(name=category)
        return redirect('category')  
    else:
        return redirect('category') 

  

def brand(request):
    brands=Brand.objects.all()
    return render(request,'admin/brand.html',{'brands':brands,'title':'Brands'})


def brandactive(request,id):
    brand=Brand.objects.get(id=id)
    
    if brand.active:
        brand.active=False
    else:
        brand.active=True
    brand.save()
    return redirect('brand')


def addbrand(request):
    if request.method=='POST':
        brand=request.POST.get('brand')
        if brand:
            Brand.objects.create(name=brand)
            
            return redirect('brand')
    else:
        return redirect('brand')

  
def editbrand(request,id):
    brand =Brand.objects.get(id=id)
    return render(request,'admin/editbrand.html',{'brand':brand,'title':'Brand'})


def editbrand_action(request):
    if request.method == "POST":
        id=request.POST.get('id')
        name=request.POST.get('editbrand')
        existing_category =Brand.objects.filter(name=name)
        if existing_category.exists():
            messages.error(request,'brand name already exists') 
            return redirect('editbrand')
        else:
            brand=Brand.objects.get(id=id)
            brand.name=name
            brand.save()
            return redirect('brand')


def coupon(request):
    coupon =Coupon.objects.all()
    return render(request,'admin/admin_coupon.html' ,{'coupon':coupon})

def addcoupon(request):
    if request.method == 'POST':
        code =request.POST.get('coupon-code')
        expiry_date =request.POST.get('expiry_date')
        discount_price =request.POST.get('discount_price')
        
        
        
        Coupon.objects.create(coupon_code=code,expiry_date=expiry_date,discount_price=discount_price)
        
        return redirect('coupon')
    else:
        return redirect('coupun')

def edit_coupon(request,id):
    coupon =Coupon.objects.get(id=id)
    return render(request,'admin/edit_coupon.html',{'coupon':coupon})

def edit_couponaction(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        code = request.POST.get('code')
        expiry_date = request.POST.get('expiry_date')
        discount_price = request.POST.get('discount_price')
        
        coupon=Coupon.objects.get(id=id)
        
        coupon.coupon_code = code
        coupon.expiry_date = expiry_date
        coupon.discount_price = discount_price
        coupon.save()
        return redirect('coupon')

    return render(request,'admin/admin_coupon.html')



def couponactive(request):
    coupons = Coupon.objects.all()
    current_date = timezone.now().date()
    
    for coupon in coupons:
        if coupon.is_expired < current_date:
            coupon.active = False
        else:
            coupon.active = True
        coupon.save()
    
    return redirect('coupon')

  
def admin_product(request):
    Products=Product.objects.all()
    return render(request,'admin/admin_product.html',{'Products':Products,'title':'Product'})

def admin_addproduct(request):
    brand=Brand.objects.all()
    category=Category.objects.all()
    context={
        'brand':brand,
        'category':category,
        'title':'Add Product'
    }
    return render(request,'admin/admin_addproduct.html',context)

def addproduct_perform(request):
    if request.method=="POST":
        name=request.POST.get('name')
        image1=request.FILES.get('img1')
        image2=request.FILES.get('img2')
        image3=request.FILES.get('img3')
        image4=request.FILES.get('img4')
        price=request.POST.get('price')
        description=request.POST.get('description')
        stock=request.POST.get('stock')
        category=request.POST.get('category')
        brand=request.POST.get('brand')
        Product.objects.create(Product_Name=name, img1=image1, img2=image2, img3=image3, img4=image4, price=price, Description=description, Stock=stock, Category_id=category, Brand_id=brand)
        return redirect('admin_product')
    else:
        return redirect('admin_product')
    
    
def admin_productview(request,id):
    product = Product.objects.get(id=id)
    return render(request,'admin/admin_productview.html',{'product':product,'title':' View Product'})


def edit_product(request,id):
    product=Product.objects.get(id=id)
    brand=Brand.objects.exclude(active=False)
    category=Category.objects.exclude(active=False)
    context={
        'product':product,
        'brand': brand,
        'category':category,
        'title':'Edit Product'
    }
    return render(request,'admin/edit_product.html',context)

def edit_productperfom(request):
    if request.method=="POST":
        id = request.POST.get('id')
        name=request.POST.get('title')
        image1=request.FILES.get('image1')
        image2=request.FILES.get('image2')
        image3=request.FILES.get('image3')
        image4=request.FILES.get('image4')
        price=request.POST.get('price')
        description=request.POST.get('description')
        stock=request.POST.get('stock')
        category=request.POST.get('category')
        brand=request.POST.get('brand')

        product=Product.objects.get(id=id)
        
        product.Product_Name=name
        product.Brand_id=brand
        product.Category_id=category
        product.price=price
        product.Stock=stock
        product.Description=description
        
        if image1 is not None:
            product.img1=image1
        if image2 is not None:
            product.img2=image2
        if image3 is not None:
            product.img3=image3
        if image4 is not None:
            product.img3=image4
            
        product.save()
        return redirect('admin_product')
    
    else:
        return redirect('admin_productview')
    

def productactive(request,id):
    product=Product.objects.get(id=id)
    
    if product.active:
        product.active=False
    else:
        product.active=True
    product.save()
    return render(request,'admin/admin_productview.html',{'product':product})

def productdelete(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect('admin_product')


def customer(request):
    customer=User.objects.all().exclude(is_superuser=True)
    return render(request,'admin/customer.html',{'customer':customer})

def customeractive(request, id):
    if request.method == 'POST':
        customer = get_object_or_404(User, id=id)
        customer.is_active = not customer.is_active
        customer.save()
    
    return redirect('customer')

    
def order(request):
    order =Order.objects.all()
    oderitem =OrderItem.objects.all
    return render(request,'admin/admin_orderview.html',{'order':order,'oderitem':oderitem})