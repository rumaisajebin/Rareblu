from django.shortcuts import render , get_list_or_404,redirect
from admin_side.models import *
from .cart import Cart
from django.db.models import Q
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

    
def home(request):
    product= Product.objects.exclude(active=False)
    return render(request,'user/home.html',{'product': product})


def search(request):
    query = request.GET.get('query')
    if query:
        product = Product.objects.filter(Q(Product_Name__icontains=query) | Q(Description__icontains=query)).exclude(active=False)
    return render(request, 'user/home.html' ,{'product':product})   

def add_to_cart(request,product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart_view')

def product_detail(request):
    product= Product.objects.exclude=False
    return render(request, 'user/cart_item_detail.html',{ 'product':product})

def cart_view(request):
    cart =Cart(request)
    return render(request, 'user/cart.html',{ 'cart':cart})

def remove_from_cart(request,product_id):
    cart =Cart(request)
    cart.remove(product_id)
    return redirect('cart_view')

def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)
    
    return redirect('cart_view')

def hx_cart_total(request):
    return render(request,'user/cart_total.html')

@login_required
def add_address(request):
    cart = Cart(request)
    user_addresses = Address.objects.filter(user=request.user)
    context={
        'cart':cart,
        'user_addresses':user_addresses
    }
    return render(request, 'user/checkout.html', context)

def addaddress_perform(request):
    if request.method == 'POST':
        name = request.POST.get('fullName')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        email = request.POST.get('email')
        phonenumber1 = request.POST.get('phonenumber1')
        phonenumber2 = request.POST.get('phonenumber2')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        Address.objects.create(
            user=request.user,
            full_name=name,
            address1=address1,
            address2=address2,
            phone_1=phonenumber1,
            phone_2=phonenumber2,
            city=city,
            pincode=pincode
        )
        return redirect('add_address')
    else:
        return render(request, 'user/checkout.html')
                      
def addressview(request,id):
    address = Address.objects.get(id=id)
    return render(request,'admin/admin_productview.html',{'address':address,'title':' View Product'})

def success(request):
    return render(request,'user/success.html')

def success2(request):
    return render(request,'user/success2.html')