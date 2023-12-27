from datetime import date, timezone
import datetime
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render , get_list_or_404,redirect
from django.urls import reverse
from admin_side.models import *
from .Carts import Cart
from django.db.models import Q
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from .form import CouponForm

# Create your views here.

def home(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    product = Product.objects.all().exclude(Q(active=False) | Q(Brand__active=False))
    
    context = {
        'category': category,
        'product': product,
        'brand': brand,
    }

    return render(request,'user/home.html',context)



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
    category_offers = CategoryOffer.objects.filter(category=product.Category, start_date__lte=date.today(), end_date__gte=date.today())
    product_offer = ProductOffer.objects.filter(product=product, start_date__lte=date.today(), end_date__gte=date.today())
    product.get_discounted_price = product.get_discounted_price() 

    context= {
        'product': product,
        'image_fields':image_fields,
        'product_offer':product_offer,
        'category_offers': category_offers
    }
    return render(request,'user/product_view.html',context)    



# filter products

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
        messages.info(request, f"{product.Product_Name} already exists in the cart.")
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
            if item:
                Wishlist.objects.filter(product=product, user=request.user).delete()
                messages.success(request, f"{item.product.Product_Name} removed from Wishlist.")
        messages.success(request, f"{item.product.Product_Name} added to cart successfully!")
    
    
        default_url = '/'
        referer = request.META.get('HTTP_REFERER', default_url)
        try:
            return redirect(referer)
        except ValueError:
            return redirect(default_url)

@login_required
def cart(request):
    cart =CartItem.objects.filter(user=request.user)
    for item in cart:
        category_offers = CategoryOffer.objects.filter(category=item.product.Category, start_date__lte=date.today(), end_date__gte=date.today())
        item.category_offers = category_offers  # Add category offers to each cart item

    total_cart_price = sum(item.total_price() for item in cart)
    coupon_form= CouponForm(request.POST)
    coupon=""
    request.session['discount_price'] = int(0)
    request.session['total_price'] =  float(total_cart_price)
    if coupon_form.is_valid():
        code = coupon_form.cleaned_data['code']
        coupon = Coupon.objects.filter(coupon_code=code, active=True)
        if Applied_coupon.objects.filter(user=request.user, coupon=code).exists():
            messages.error(request, f"The Coupon {code} is Already used before")
        else:
            try:
                current_time = datetime.datetime.now()
                coupon = Coupon.objects.get(coupon_code=code, is_expired__gte=current_time, active=True)
                discounted_price = total_cart_price - coupon.discount_price
                
                if discounted_price >= 0:
                    total_cart_price = discounted_price
                    request.session['coupon'] = code
                    request.session['discount_price'] = coupon.discount_price
                    request.session['total_price'] = total_cart_price
                    messages.success(request, f'Coupon {code} applied successfully!')
                else:
                    messages.error(request, f"The coupon {code} cannot reduce the total below zero.")
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code.')

    return render(request, 'user/cart.html',{'cart':cart, 'total_cart_price': total_cart_price,'coupon_form':coupon_form,'coupon':coupon})


def update_cart(request, id, action):
    cart_item = get_object_or_404(CartItem, user=request.user, product=id)

    if action == 'increment':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrement':
        cart_item.quantity -= 1
        cart_item.save()

    if cart_item.quantity > cart_item.product.Stock:
        messages.error(request, f'{cart_item.product.Product_Name} is out of stock.')
        return redirect('cart')
    
    if not cart_item.product.active:
        messages.error(request, f'{cart_item.product.Product_Name} is inactive.')
        return redirect('cart')

    if cart_item.quantity == 0:
        print('cartdelete')
        cart_item.delete()
    
    default_url = '/'
    referer = request.META.get('HTTP_REFERER', default_url)

    return redirect(referer)

def remove_item(request,id):
    product = CartItem.objects.get(id=id)
    if product:
        product.delete()
    return redirect('cart')
   
def hx_menu_cart(request):
    return render(request, 'user/menu_cart.html')


def hx_cart_total(request):
    return render(request, 'user/cart_total.html')


# Address

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
        
                      
def addressview(request):
    address = Address.objects.filter(user=request.user)
    return render(request,'user/address.html',{'address':address})


def edit_address(request, id):
    address = Address.objects.get(id=id)
    return render(request, 'user/edit_address.html', {'address': address,'id':id})

def edit_addressperform(request, id):
    if request.method == 'POST':
        name = request.POST.get('fullName')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        email = request.POST.get('email')
        phonenumber1 = request.POST.get('phonenumber1')
        phonenumber2 = request.POST.get('phonenumber2')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        address = Address.objects.get(id=id)
        address.full_name = name
        address.address1 = address1
        address.address2 = address2
        address.phone_1 = phonenumber1
        address.phone_2 = phonenumber2
        address.city = city
        address.pincode = pincode
        address.save()
        
        return redirect('addressview')
    
    else:
        return render(request,'user/edit_address.html')
    
    
def addressdelete(request,id):
    address=Address.objects.get(id=id)
    address.delete()
    return render(request,'user/address.html')


@login_required
def checkout(request):
    cart =CartItem.objects.filter(user=request.user)
    for item in cart:
        category_offers = CategoryOffer.objects.filter(category=item.product.Category, start_date__lte=date.today(), end_date__gte=date.today())
        item.category_offers = category_offers  # Add category offers to each cart item
    total_cart_price = request.session.get('total_price')
    discount_price = request.session.get('discount_price', 0)
    user_addresses = Address.objects.filter(user=request.user)
    context ={'cart':cart,
        'user_addresses':user_addresses,
        'total_cart_price': total_cart_price,
        'discount_price':discount_price}
    return render(request, 'user/checkout.html',context)


def place_order(request):
    cart =CartItem.objects.filter(user=request.user)
    total_cart_price =  request.session.get('total_price')
    host = request.get_host()
    
    if not cart:
        messages.error(request, 'Your cart is empty. Please add items before placing an order.')
        return redirect('cart')


    for cart_item in cart:
        if cart_item.quantity > cart_item.product.Stock:
            messages.error(request, f'{cart_item.product.Product_Name} is out of stock.')
            return redirect('cart')
        if cart_item.product.active == False:
            messages.error(request, f'{cart_item.product.Product_Name} is out of stock.')
            return redirect('cart')
    
    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('paymentmethod')

        if payment_method == 'COD':
            order = Order.objects.create(
                user=request.user,
                address_id=address,
                total_paid=total_cart_price,
                billing_status=payment_method,
            )

            for item in cart:
                product = item.product
                quantity = item.quantity
                price = item.product.price * quantity

                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
                product.Stock -= item.quantity 
                product.save()

            cart.delete()
            return render(request,'user/success2.html')
        
        elif payment_method == 'Wallet':
            user = request.user
            wallets = Wallet.objects.filter(user=user)
            wallet_balance = sum(wallet.total_balance() for wallet in wallets)

            if wallet_balance > total_cart_price:
                coupon = request.session.get('coupon')
                order =Order.objects.create(user=user, address_id=address,  total_paid=total_cart_price, billing_status=payment_method,paid=True)
                Applied_coupon.objects.create(user=user, coupon=coupon)
                Wallet.objects.create(user=user, amount=order.total_paid, balance_type=Wallet.DEBIT)

                for item in cart:
                    product = item.product
                    quantity = item.quantity
                    price = item.product.price * quantity

                    OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
                    product.Stock -= item.quantity 
                    product.save()
                cart.delete()
                return redirect('order_listing')
            else:
                messages.error(request,'wallet have no much money')
                return redirect('checkout')
            
        else:
            items = []
            for item in cart:
                product = item.product
                quantity = item.quantity
                price = item.product.price * quantity

                item_dict = {
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                }
                items.append(item_dict)

            paypal_checkout = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": total_cart_price,
                "currency_code": "USD",
                "item_name": items,
                "invoice": uuid.uuid4,
                "notify_url":f"https://{host}{reverse('paypal-ipn')}",
                "return": f"http://{host}{(reverse('paymentsuccessful',kwargs ={'address':address}))}",
                "cancel_return": f"http://{host}{(reverse('paymentfailed'))}",
                }
            paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
            context = {'paypal_payment':paypal_payment}
            return render(request, "user/success.html",context)
    else:
        print('Not placed')
        return redirect('cart')
    

def paymentsuccessful(request,address):
    cart =CartItem.objects.filter(user=request.user)
    total_cart_price =  request.session.get('total_price')
    coupon = request.session.get('coupon')
    Applied_coupon.objects.create(user=request.user, coupon=coupon)
    
    order = Order.objects.create(
            user=request.user,
            address_id=address,
            total_paid=total_cart_price,
            billing_status='paypal',
            paid=True
            )
    for item in cart:
        product = item.product
        quantity = item.quantity
        price = item.product.price * quantity

        OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
        product.Stock -= item.quantity 
        product.save()
    cart.delete()
    
    return render(request,'user/paymentsuccessful.html')


def paymentfailed(request):
    return HttpResponse("Payment failed or canceled. Please try again.")



def success(request):
    return render(request,'user/success.html')



def success2(request):
    return render(request,'user/success2.html')



def view_coupons(request):
    active_coupons = Coupon.objects.filter(active=True)
    applied_coupons = Applied_coupon.objects.filter(user=request.user)
    return render(request, 'user/profile.html', {'active_coupons': active_coupons,'applied_coupons':applied_coupons})


# order

def order_listing(request):
    order = Order.objects.filter(user=request.user)
    return render(request, 'user/order_listing.html', {'order': order})


def order_detailview(request,id):
    order = Order.objects.get(id=id)
    return render(request, 'user/order_detailview.html', {'order': order})


def cancel_order(request,order_id):
    order = Order.objects.get(id=order_id)
    if order.active:
        order.active=False
    else:
        order.active=True
    order.status='cancelled'
    order.save()
    if order.billing_status in ['paypal', 'wallet']:
        # Add the amount back to the user's wallet
        Wallet.objects.create(user=order.user, amount=order.total_paid, order=order, balance_type=Wallet.CREDIT,transaction_description="Cancelled amount.")
    if order.status == 'cancelled':
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            item.product.Stock += item.quantity
            item.product.save()
        
    return redirect('order_listing')

    
def return_order(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    existing_return =Returnedproduct.objects.filter(order=order)
    if existing_return:
        existing_return=existing_return.get(order=order)
    else:
        if request.method == 'POST' and not existing_return:
            reason = request.POST.get('reason')
            returnedproduct = Returnedproduct.objects.create(order=order,reason=reason)
            messages.success(request,'Return requested succesfully.')
            return redirect('order_listing')
    if existing_return and existing_return.return_status == existing_return.RETURNED:
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            item.product.Stock += item.quantity
            item.product.save()
    return render(request,'user/return_order.html',{'order':order,'existing_return':existing_return})


@login_required
def wallet(request):
    wallet = Wallet.objects.filter(user=request.user)
    total_balance = sum(wallet.total_balance() for wallet in wallet)
    return render(request, 'user/wallet.html', {'wallet': wallet, 'total_balance':total_balance})


# Wishlist
@login_required
def wishlist(request):
    wish = Wishlist.objects.filter(user=request.user)
    return render(request,'user/wishlist.html',{'wish':wish})

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    wishlist_item, created = Wishlist.objects.get_or_create(product=product, user=request.user)

    if not created:
        messages.info(request, f"{product.Product_Name} already exists in the wishlist.")
    
    try:
        return redirect(wishlist)
    except ValueError:
        return redirect(cart)
        
def wish_remove(request,id):
    wishlist_item =Wishlist.objects.get(id=id)
    if request.user.is_authenticated and wishlist_item.user == request.user:
        wishlist_item.delete()
        messages.success(request, "Item removed from wishlist.")
    else:
        messages.error(request, "You don't have permission to remove this item from the wishlist.")
    return redirect('wishlist')

def remove_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id)
    product_in_wishlist = Wishlist.objects.filter(product=cart_item.product, user=request.user)
    
    if request.user.is_authenticated and cart_item.user == request.user:
        cart_item.delete()
        messages.success(request, "Item removed from the cart.")
        
        # Remove from wishlist if exists
        if product_in_wishlist.exists():
            product_in_wishlist.delete()
            messages.success(request, "Item removed from the wishlist.")
    else:
        messages.error(request, "You don't have permission to remove this item from the cart.")
    
    return redirect('cart')  
