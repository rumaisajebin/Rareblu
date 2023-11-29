from datetime import timezone
from django.shortcuts import get_object_or_404, render , get_list_or_404,redirect
from admin_side.models import *
from .Carts import Cart
from django.db.models import Q
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.

def home(request):
    product= Product.objects.exclude(active=False)
    return render(request,'user/home.html',{'product': product})



def search(request):
    query = request.GET.get('query')
    
    if query:
        product = Product.objects.filter(Q(Product_Name__icontains=query) | Q(Description__icontains=query)).exclude(active=False)
    return render(request, 'user/home.html' ,{'product':product})



def product(request):
    product= Product.objects.exclude(active=False)
    category =Category.objects.all()
    brand =Brand.objects.all()
        
    context = {
        'product': product,
        'category': category,
        'brand': brand,
    }
    return render(request,'user/product_listing.html', context)

def product_view(request,id):
    product =Product.objects.get(id=id)
    image_fields = [product.img1, product.img2, product.img3, product.img4]
    return render(request,'user/product_view.html',{'product':product,'image_fields':image_fields})    


def price_filter(request):
    product =Product.objects.none()
    category =Category.objects.all()
    brand =Brand.objects.all()
    
    if request.method == "POST":
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        s_category=request.POST.get('category')
        s_brand=request.POST.get('brand')

        conditions = Q()
        
        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)

                if max_price < min_price:
                    messages.error(request, "Maximum price should be greater than or equal to the minimum price.")
                    return render(request, "user/product_listing.html", {'product': product, 'category': category, 'brand': brand})
                
                conditions &= Q(price__range=(min_price, max_price))
                
            except ValueError:
                messages.error(request, "Invalid price values")
                return render(request, "user/product_listing.html", {'product': product, 'category': category, 'brand': brand})

            product = Product.objects.filter(
                price__gte=min_price, price__lte=max_price, active=True)

        if s_category:
            conditions &= Q(Brand=s_category)
        
        if s_brand:
            conditions &= Q(Brand=s_brand)
        product = Product.objects.filter(conditions)
    context = {
        'product': product,
        'category': category,
        'brand': brand,
    }
    return render(request,"user/filtered_product_list.html",context)




@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    if CartItem.objects.filter(product_id=id).exists():
        default_url = '/'
        referer = request.META.get('HTTP_REFERER', default_url)
        try:
            return redirect(referer)
        except ValueError:
            return redirect(default_url)
    else:
        item = CartItem.objects.create(product=product, quantity=1)
        if request.user:
            item.user = request.user
            item.save()
        messages.success(request, f"{Product.Product_Name} added to cart successfully!")
        default_url = '/'
        referer = request.META.get('HTTP_REFERER', default_url)
        try:
            return redirect(referer)
        except ValueError:
            return redirect(default_url)


def cart(request):
    cart =CartItem.objects.filter(user=request.user)
    total_cart_price = sum(item.total_price() for item in cart)
    return render(request, 'user/cart.html',{'cart':cart, 'total_cart_price': total_cart_price})


def update_cart(request, id, action):
    cart = get_object_or_404(CartItem, product=id)
    if action == 'increment':
        cart.quantity += 1
    elif action == 'decrement':
        cart.quantity -= 1

    cart.save()
    if cart.quantity == 0:
        cart.delete()

    default_url = '/'
    referer = request.META.get('HTTP_REFERER', default_url)

    try:
        return redirect(referer)
    except ValueError:
        return redirect(default_url)

# def remove(request,id):
#     cart = CartItem.objects.get(id=id)
#     cart.delete()
#     return redirect(cart)

def hx_menu_cart(request):
    return render(request, 'user/menu_cart.html')


def hx_cart_total(request):
    return render(request, 'user/cart_total.html')


@login_required
def checkout(request):
    cart =CartItem.objects.filter(user=request.user)
    total_cart_price = sum(item.total_price() for item in cart)
    user_addresses = Address.objects.filter(user=request.user)
    return render(request, 'user/checkout.html',{'cart':cart, 'user_addresses':user_addresses, 'total_cart_price': total_cart_price})


def place_order(request):
    cart =CartItem.objects.filter(user=request.user)
    total_cart_price = sum(item.total_price() for item in cart)
    
    if not cart:
        messages.error(request, 'Your cart is empty. Please add items before placing an order.')
        return redirect('cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('paymentmethod')

        if payment_method == 'COD':
            order = Order.objects.create(
                user=request.user,
                address_id=address,
                total_paid=total_cart_price,
                billing_status=payment_method
            )

            for item in cart:
                product = item.product
                quantity = item.quantity
                price = item.product.price * quantity

                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            cart.delete()
            return render(request,'user/user_profile.html')
        else:
       
            return render(request, "success.html")
    else:
        print('Not placed')
        return redirect('cart')



def add_address(request):
    cart = Cart(request)
    user_addresses = Address.objects.filter(user=request.user)
    return render(request, 'user/add_address.html',  {'cart':cart,'user_addresses':user_addresses})


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
        return redirect('checkout')
    
    else:
        return render(request, 'user/add_address.html')
        
                      
def addressview(request,id):
    address = Address.objects.get(id=id)
    return render(request,'user/checkout.html',{'address':address})


def edit_address(request, id):
    address = Address.objects.get(id=id)
    return render(request, 'user/edit_address.html', {'address': address,'id':id})


def edit_addressperform(request,id):
    
    if request.method == 'POST':
        name = request.POST.get('fullName')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        email = request.POST.get('email')
        phonenumber1 = request.POST.get('phonenumber1')
        phonenumber2 = request.POST.get('phonenumber2')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        address=Address.objects.get(id=id)
        address.full_name=name,
        address.address1=address1,
        address.address2=address2,
        address.phone_1=phonenumber1,
        address.phone_2=phonenumber2,
        address.city=city,
        address.pincode=pincode
        address.save()
        return redirect('edit_address',id=id)
    
    else:
        return render(request,'user/edit_address.html')
    
    
def addressdelete(request,id):
    address=Address.objects.get(id=id)
    address.delete()
    return render(request,'user/checkout.html')



def success(request):
    return render(request,'user/success.html')



def success2(request):
    return render(request,'user/success2.html')



def confirm_order(request):
    if request.method == 'POST':
        payment_method =request.POST.get('paymentmethod')
        
        if payment_method == 'cash_ondelivery':
            return render(request,'user/success2.html')
        elif payment_method == 'PayPal':
            return render (request,'user/success.html')
        else:
            pass
    else:
        return render(request,'checkout,html')

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code, active=True)
            # Apply coupon logic here, for example, adjusting the cart total
            # cart.apply_coupon(coupon)
            return redirect('checkout')  # Redirect to checkout or cart page after applying the coupon
        except Coupon.DoesNotExist:
            error_message = "Invalid coupon code. Please try again."
            return render(request, 'user/coupons.html', {'error_message': error_message})
    return redirect('user_coupons')


def view_coupons(request):
    active_coupons = Coupon.objects.filter(active=True)
    return render(request, 'user/coupons.html', {'active_coupons': active_coupons})


    
# def orderlisting(request):
#     order=Order.objects.filter()
#     return render(request,'user/user_profile.html')