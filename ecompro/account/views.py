from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.views.decorators.cache import never_cache
from django.conf import settings
import pyotp
from .otp import send_otp
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from admin_side.models import *


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
    return redirect('log_in')

