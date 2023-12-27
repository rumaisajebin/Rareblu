from asyncio import exceptions
from datetime import date, timedelta, timezone
import datetime
from decimal import Decimal
from imaplib import _Authenticator
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect,get_list_or_404
from admin_side.models import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from cart.models import *
from django.contrib.auth.decorators import login_required

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
# Create your views here..


from django.http import HttpResponseForbidden

def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            # User is a superadmin, proceed with the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not a superadmin, return forbidden response
            return HttpResponseForbidden("Permission Denied: Superadmin required")

    return wrapper

@superadmin_required
def admin_home(request):
    ncustomer=User.objects.all().exclude(is_superuser=True).count()
    nproduct = Product.objects.all().count()
    norder = Order.objects.all().count()
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)
    one_year_ago = today - timedelta(days=365)

    sales_per_day = Order.objects.filter(created__date=today).count()
    sales_per_week = Order.objects.filter(created__date__gte=one_week_ago).count()
    sales_per_year = Order.objects.filter(created__date__gte=one_year_ago).count()

    context = {
        'title': 'Dashboard',
        'ncustomer': ncustomer,
        'nproduct': nproduct,
        'norder': norder,
        'sales_per_day': sales_per_day,
        'sales_per_week': sales_per_week,
        'sales_per_year': sales_per_year,
    }
    return render(request,'admin/admin_dashboard.html',context)


# Category

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

  
# Brand

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


# Coupon

def coupon(request):
    coupon =Coupon.objects.all()
    return render(request,'admin/admin_coupon.html' ,{'coupon':coupon,'title':'Coupon'})


def addcoupon(request):
    if request.method == 'POST':
        code =request.POST.get('coupon-code')
        expiry_date =request.POST.get('expiry_date')
        discount_price =request.POST.get('discount_price')
                     
        Coupon.objects.create(coupon_code=code,is_expired =expiry_date,discount_price=discount_price)
        
        return redirect('coupon')
    else:
        return redirect('coupun')


def edit_coupon(request,id):
    coupon =Coupon.objects.get(id=id)
    return render(request,'admin/edit_coupon.html',{'coupon':coupon,'title':'Edit Coupon'})

def edit_couponaction(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        code = request.POST.get('code')
        expiry_date = request.POST.get('expiry_date')
        discount_price = request.POST.get('discount_price')
        
        coupon=Coupon.objects.get(id=id)
        
        coupon.coupon_code = code
        coupon.is_expired = expiry_date
        coupon.discount_price = discount_price
        coupon.save()
        return redirect('coupon')

    return render(request,'admin/admin_coupon.html')


# Product

def admin_product(request):
    if request.user.is_superuser:
        Products=Product.objects.all()
        return render(request,'admin/admin_product.html',{'Products':Products,'title':'Product'})
    else:
        return HttpResponseForbidden("Permission Denied: Superadmin required")
    
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
    
    
def admin_productview(request, id):
    product = Product.objects.get(id=id)
    product.get_discounted_price = product.get_discounted_price()  # Calculate discounted price
    category_offer = CategoryOffer.objects.filter(category=product.Category, start_date__lte=date.today(), end_date__gte=date.today())
    product_offer = ProductOffer.objects.filter(product=product, start_date__lte=date.today(), end_date__gte=date.today())
    context = {
        'product': product,
        'title': 'View Product',
        'product_offer': product_offer,
        'category_offer': category_offer
    }
    return render(request, 'admin/admin_productview.html', context)




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


# Coustmer

def customer(request):
    customer=User.objects.all().exclude(is_superuser=True)
    return render(request,'admin/customer.html',{'customer':customer})


def customeractive(request, id):
    if request.method == 'POST':
        customer = get_object_or_404(User, id=id)
        customer.is_active = not customer.is_active
        customer.save()
    
    return redirect('customer')



# Order

def order(request):
    order =Order.objects.all()
    orderitem =OrderItem.objects.all()
    return render(request,'admin/admin_orderview.html',{'order':order,'orderitem':orderitem,'title':'Order'})


def order_update(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        if new_status:
            order.status = new_status
            
            if new_status == 'delivered' and order.billing_status=='COD':
                order.paid=True
                order.save()
                
            if (new_status == 'cancelled') and order.paid==True:
                order_items = OrderItem.objects.filter(order=order)
                for item in order_items:
                    item.product.Stock += item.quantity
                    item.product.save()

                Wallet.objects.create(user=order.user, amount=order.total_paid, order=order)

            order.save()
            return redirect('order_view', order_id=order_id)
    return render(request,'admin/order_view.html', {'order': order})
    

def order_view(request,order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    order_status_choices = [
        (status, status_display) for status, status_display in Order.ORDER_STATUS_CHOICES if status != 'returned'
    ]
    context = {'title':'Order Details',
             'order':order,
             'order_items':order_items,
             'order_status_choices':order_status_choices}
    return render(request,'admin/order_view.html',context)


# Order Return

def order_return(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    if request.POST.get('action') == 'approve':
        order.is_return_requested = False
        order.is_return_approved = True
        order.save()
    elif request.POST.get('action')=='reject':
        order.is_return_requested=False
        order.save()
    return redirect('order',order_id=order.id)

def returnedorders(request):
    returned = Returnedproduct.objects.all()
    return render(request,'admin/returnedorders.html',{'returned':returned,'title':'Returned Orders'})
    
def returned_details(request, id):
    returned = Returnedproduct.objects.get(id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            returned.return_status = new_status
            order = returned.order
            if new_status == returned.RETURNED:
                order.status = order.RETURNED
                order.save()
                
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                item.product.Stock += item.quantity
                item.product.save()
            Wallet.objects.create(user=order.user, amount=order.total_paid, order=order,transaction_description="Returned amount.")
            returned.save()
            
            return redirect('returned_details', id=id)
    return render(request, "admin/return_view.html", {'returned':returned,'title':'Returned Order Details'})


# category Offer

def category_Offer(request):
    categoryoffer =CategoryOffer.objects.all()
    category=Category.objects.exclude(active=False)
    return render(request,'admin/admin_categoryoffer.html',{'title':'Category Offer','categoryoffer':categoryoffer,'category':category})

def add_category_Offer(request):
    category=Category.objects.exclude(active=False)
    if request.method == 'POST':
        category = request.POST.get('category')
        percent_offer = request.POST.get('percent_offer')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        CategoryOffer.objects.create(
            category_id=category,
            percent_offer=percent_offer,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('category_Offer')
    else:
        return render(request,'admin/admin_categoryoffer.html',{'category':category})


def edit_category_offer(request, offer_id):
    category_offer = get_object_or_404(CategoryOffer, id=offer_id)
    categories = Category.objects.exclude(active=False)

    if request.method == 'POST':
        category = request.POST.get('category')
        percent_offer = request.POST.get('percent_offer')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        category_offer.category_id = category
        category_offer.percent_offer = percent_offer
        category_offer.start_date = start_date
        category_offer.end_date = end_date
        category_offer.save()

        return redirect('category_Offer')
    else:
        return render(request, 'admin/edit_category_offer.html', {'category_offer': category_offer, 'categories': categories})

def delete_category_Offer(request,offer_id):
    category_offer = get_object_or_404(CategoryOffer, id=offer_id)
    category_offer.delete()
    return redirect('category_Offer')

# product Offer

def product_Offer(request):
    productoffer =ProductOffer.objects.all()
    product=Product.objects.exclude(active=False)
    return render(request,'admin/admin_productoffer.html',{'title':'Product Offer','productoffer':productoffer,'product':product})

def add_product_Offer(request):
    product=Product.objects.exclude(active=False)
    if request.method == 'POST':
        product = request.POST.get('product')
        percent_offer = request.POST.get('percent_offer')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        ProductOffer.objects.create(
            product_id=product,
            percent_offer=percent_offer,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('product_Offer')
    else:
        return render(request,'admin/admin_productoffer.html',{'product':product})


def edit_product_offer(request, offer_id):
    product_offer = get_object_or_404(ProductOffer, id=offer_id)
    product = Product.objects.exclude(active=False)

    if request.method == 'POST':
        product = request.POST.get('product')
        percent_offer = request.POST.get('percent_offer')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        product_offer.product_id = product
        product_offer.percent_offer = percent_offer
        product_offer.start_date = start_date
        product_offer.end_date = end_date
        product_offer.save()

        return redirect('product_Offer')
    else:
        return render(request, 'admin/edit_product_offer.html', {'title':'Edit Product Offer','product_Offer': product_offer, 'product': product})

def delete_product_Offer(request,offer_id):
    product_Offer = get_object_or_404(ProductOffer, id=offer_id)
    product_Offer.delete()
    return redirect('product_Offer')

# Salesreport

def salesreport(request):
    order = Order.objects.filter(status='delivered')
    total_sales = sum(ord.total_paid for ord in order)
    order_items = OrderItem.objects.filter(order__in=order)
    item_quantity_sold = sum(item.quantity for item in order_items)

    if request.method == 'POST' and 'generate_pdf' in request.POST:
        pdf = generate_sales_report_pdf(order, total_sales, order_items, item_quantity_sold)

        response = HttpResponse(content_type='application/pdf')
        d = datetime.today().strftime('%y-%m-%d')
        response['Content-Disposition'] = f'inline; filename="{d}_sales_report.pdf"'
        response.write(pdf)
        return response

    context ={
        'title':'Sales Report',
        'order':order,
        'total_sales':total_sales,
        'order_items':order_items,
        'item_quantity_sold':item_quantity_sold,
    }
    return render(request, 'admin/admin_salesreport.html', context)


def filter_salesreport(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                if end_date < start_date:
                    messages.error(request, "End date should be greater than or equal to the Start date.")
                    return redirect('salesreport')

                # Apply date range filter to Order queryset
                order = Order.objects.filter(created__date__range=(start_date, end_date)).filter(status='delivered')
                print(order)
                # Pass the filtered queryset to the template
                context = {
                    'title': 'Sales Report',
                    'order': order,
                    'start_date': start_date,
                    'end_date': end_date,
                }

                return render(request, 'admin/admin_salesreport.html', context)

            except ValueError:
                messages.error(request, "Invalid Date")
                return redirect('salesreport')

    return redirect('salesreport')


from datetime import datetime
def generate_sales_report_pdf(order, total_sales, order_items, item_quantity_sold, start_date=None, end_date=None):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Start writing the PDF here
    p.setFont("Helvetica", 15)
    p.drawString(50, 800, f"Sales Report - {datetime.today().strftime('%Y-%m-%d')}")

    # Create a table structure with borders
    table_headers = [
        "Order ID", "Customer", "Total Paid", "Status", "Product", "Price", "Quantity Sold", "Date"
    ]
    col_widths = [70, 100, 80, 70, 120, 50, 90, 100]

    # Set initial y-coordinate and draw table headers
    y_start = 750
    y = y_start
    x = 50

    for i, header in enumerate(table_headers):
        p.drawString(x, y, header)
        x += col_widths[i]
    y -= 20

    # Draw table borders
    p.rect(50, y, sum(col_widths), y_start - y, stroke=1, fill=0)

    # Loop through orders and items to fill the table
    for ord in order:
        for item in ord.items.all():
            x = 50
            p.drawString(x, y, str(ord.id))
            x += col_widths[0]

            p.drawString(x, y, str(ord.user.username))
            x += col_widths[1]

            p.drawString(x, y, f"${ord.total_paid}")
            x += col_widths[2]

            p.drawString(x, y, str(ord.status))
            x += col_widths[3]

            p.drawString(x, y, str(item.product.Product_Name))
            x += col_widths[4]

            p.drawString(x, y, f"${item.price}")
            x += col_widths[5]

            p.drawString(x, y, str(item.quantity))
            x += col_widths[6]

            p.drawString(x, y, str(ord.created))
            y -= 20

    p.setTitle(f'Sales Report')

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf


# # Banner

# def admin_banner(request):
#     if request.user.is_superuser:
#         banners = Banner.objects.all()
#         return render(request, 'admin/admin_banner.html', {'banners': banners, 'title': 'Banner'})
#     else:
#         return HttpResponseForbidden("Permission Denied: Superadmin required")

# def admin_addbanner(request):
#     # Assuming 'brand' and 'category' need to be passed into the context
#     context = {
#         'brand': 'YourBrand',  # Replace with actual brand data
#         'category': 'YourCategory',  # Replace with actual category data
#         'title': 'Add Banner'
#     }
#     return render(request, 'admin/add_banner.html', context)

# def add_bannerperform(request):
#     if request.method == "POST":
#         bimg = request.FILES.get('bimg')
#         title = request.POST.get('title')
#         text = request.POST.get('text')
#         link = request.POST.get('link')
#         is_active = request.POST.get('is_active')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
        
#         Banner.objects.create(bimg=bimg, title=title, text=text, link=link, is_active=is_active,
#                               start_date=start_date, end_date=end_date)
#         return redirect('admin_banner')
#     else:
#         return redirect('admin_banner')

# def admin_bannerview(request, id):
#     banner = get_object_or_404(Banner, id=id)
#     context = {
#         'banner': banner,
#         'title': 'View Banner',
#     }
#     return render(request, 'admin/admin_bannerview.html', context)

# def edit_banner(request, id):
#     banner = get_object_or_404(Banner, id=id)
#     context = {
#         'banner': banner,
#         'title': 'Edit Banner'
#     }
#     return render(request, 'admin/edit_banner.html', context)

# def edit_bannerperform(request, id):
#     banner = get_object_or_404(Banner, id=id)
#     if request.method == "POST":
#         bimg = request.FILES.get('bimg')
#         title = request.POST.get('title')
#         text = request.POST.get('text')
#         link = request.POST.get('link')
#         is_active = request.POST.get('is_active')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')

#         banner.bimg = bimg
#         banner.title = title
#         banner.text = text
#         banner.link = link
#         banner.is_active = is_active
#         banner.start_date = start_date
#         banner.end_date = end_date
#         banner.save()
#         return redirect('admin_banner')
#     else:
#         return redirect('admin_banner_view', id=id)

# def banner_active(request, id):
#     banner = get_object_or_404(Banner, id=id)
#     banner.is_active = not banner.is_active
#     banner.save()
#     return redirect('admin_banner')