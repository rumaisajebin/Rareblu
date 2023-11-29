from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseForbidden,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
import pyotp
from .otp import send_otp
from admin_side.models import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from cart.models import *

def otp_page(request):
    return render(request,'emailotp.html')


def otp(request):
    if request.method == 'POST':
        user_data = request.session.get('user_datas')
        otp = request.POST.get('otp')
        otp_key = request.session.get('otp_key')
        otp_valid = request.session.get('otp_valid')
        if otp_key and otp_valid is not None:
            valid_otp = datetime.fromisoformat(otp_valid)
            if valid_otp > datetime.now():
                totp = pyotp.TOTP(otp_key, interval=60)
                if totp.verify(otp):
                    User.objects.create_user(**user_data)
                    clear_session(request)
                    return redirect('home')
                else:
                    clear_session(request)
                    messages.error(request, 'Invalid Otp')
                    return redirect('otp_page')
            else:
                clear_session(request)
                messages.error(request, 'Otp expired')
                return redirect('sign_up')
        else:
            clear_session(request)
            messages.error(request, 'Didnt get any otp')
            return redirect('sign_up')
    return render(request, "emailotp.html")


def clear_session(request):
    key = ['otp_key', 'otp_valid', 'user_data','email']
    for key in key:
        if key in request.session:
            del request.session[key]



@never_cache         
def sign_up(request):
    if request.method =='POST':
    
        first_name =request.POST.get('firstname')
        last_name =request.POST.get('lastname')
        username =request.POST.get('username')
        email =request.POST.get('email')
        password =request.POST.get('password')
        confirm_password =request.POST.get('confirm_password')
            
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username exists')
            return redirect ('sign_up')
        elif password!=confirm_password:    
            messages.error(request,'Password and confirm password is not matching')
            return redirect('sign_up')
        else:
            request.session['email'] = email
            request.session['user_datas'] = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password': password
            }
            send_otp(request)
            # user_data.objects.create(first_name=first_name,last_name=last_name,username=username,password=password,email=email)
            return render(request,'emailotp.html')
    else:
        return render(request,'signup.html')
    



def log_in(request):
    return render(request, 'login.html')


   
@never_cache
def log_in_perform(request):
    if request.method == 'POST':
        # form = AuthenticationForm(data=request.POST)
        # if form.is_valid():
        username =request.POST.get('username')
        password =request.POST.get('password')
        usr_obj =authenticate(request,username=username,password=password)
        if usr_obj is not None:
            login(request,usr_obj)
            if usr_obj.is_superuser:
                # request.session['usertype'] = 'admin'
                return redirect('admin_home')
            else:
                return redirect('home')
        
        else:
            messages.error(request,'Username or Password is invalid')
            return HttpResponseRedirect('log_in')
    else:
        return HttpResponse("method not allowed")



def log_out(request):
    logout(request)
    return redirect('home')



def profile(request):
    order = Order.objects.filter(user=request.user)
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to view this page.")

    try:
        u_profile = User_Profile.objects.get(user=request.user)
    except User_Profile.DoesNotExist:
        u_profile = User_Profile.objects.create(user=request.user)

    return render(request, 'user/user_profile.html', {'u_profile': u_profile,'order':order})




@login_required
def editprofile(request):
    u_profile = get_object_or_404(User_Profile, user=request.user)

    if request.method == 'POST':
        profile_photo = request.FILES.get('profilepic')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenumber')

        if profile_photo:
            u_profile.profile_photo = profile_photo

        u_profile.address = address
        u_profile.PhoneNumber = phone_number
        u_profile.save()

        return redirect('profile')  # Redirect to the profile view after successful update

    return render(request, 'user/edit_profile.html', {'u_profile': u_profile})


@login_required
def edit_profile_action(request):
    u_profile = get_object_or_404(User_Profile, user=request.user)

    if request.method == 'POST':
        profile_photo = request.FILES.get('profilepic')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenumber')
        
        if profile_photo:
            u_profile.profile_photo = profile_photo

        u_profile.address = address
        u_profile.PhoneNumber = phone_number
        u_profile.save()

    return render('profile')


    