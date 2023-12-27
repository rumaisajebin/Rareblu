from datetime import datetime, timezone
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseForbidden,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
import pyotp
from .otp import send_otp
from admin_side.models import *
from django.contrib.auth.decorators import login_required
from auth_app.models import User_Profile,User,Referral
from django.shortcuts import get_object_or_404
from cart.models import *
from django.contrib.auth.hashers import make_password


def otp_page(request):
    return render(request,'emailotp.html')

def otp(request):
    if request.method == 'POST':
        user_data = request.session.get('user_datas')
        otp = request.POST.get('otp')
        otp_key = request.session.get('otp_key')
        otp_valid = request.session.get('otp_valid')
        referral_code = request.session.get('referral_code')
        if otp_key and otp_valid is not None:
            valid_otp = datetime.fromisoformat(otp_valid)
            if valid_otp > datetime.now():
                totp = pyotp.TOTP(otp_key, interval=60)
                if totp.verify(otp):
                    new_user = User.objects.create_user(**user_data)
                    Wallet.objects.create(user=new_user, amount=10, transaction_description="Welcome bonus.")
                    handle_referral(request, new_user)      
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
        messages.error(request, 'Didn\'t get any otp')
        return redirect('sign_up')
    return render(request, "emailotp.html")

def handle_referral(request, new_user):
    referral_code = request.session.get('referral_code')
    if referral_code:
        try:
            referral = Referral.objects.get(referal_code=referral_code)
            referrer_profile = User_Profile.objects.get(referral=referral)
            referrer_wallet, _ = Wallet.objects.get_or_create(user=referrer_profile.user, defaults={'amount': 0, 'transaction_description': "Referrer's initial wallet"})
            referrer_wallet.amount += 50  # Adjust the amount based on your referral reward
            referrer_wallet.save()

            referred_user_wallet, _ = Wallet.objects.get_or_create(user=new_user, defaults={'amount': 0, 'transaction_description': "Referred user's initial wallet"})
            referred_user_wallet.amount += 10  # Adjust the amount based on your referral reward
            referred_user_wallet.save()

            del request.session['referral_code']
        except (Referral.DoesNotExist, User_Profile.DoesNotExist):
            pass


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
        referral_code = request.POST.get('referral_code')
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
            if referral_code:
                request.session['referral_code'] = referral_code
                print("Referral code stored in session:", referral_code)
            send_otp(request)
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
                request.session['usertype'] = 'admin'
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


@login_required
def profile(request):
    try:
        u_profile = User_Profile.objects.get(user=request.user)
    except User_Profile.DoesNotExist:
        # If profile doesn't exist, create a new one
        u_profile = User_Profile.objects.create(user=request.user)
    
    if not u_profile.referral:
        # Generate referral code for the user
        referral_code = Referral.generate_referral_code(request.user.email, request.user.id)

        # Create a Referral instance
        referral = Referral.objects.create(referal_code=referral_code)
        print(referral)
        # Assign the Referral instance to the user's profile
        u_profile.referral = referral
        u_profile.save()
    
    order = Order.objects.filter(user=request.user)
    current_date = datetime.now(timezone.utc)
    active_coupon = Coupon.objects.filter(active=True, is_expired__gte=current_date)
    return render(request, 'user/user_profile.html', {'order': order, 'u_profile': u_profile, 'active_coupon': active_coupon})






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


def change_password(request):
    if request.method == 'POST':
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        user=request.user
        update_session_auth_hash(request, user)
        
        if authenticate(username=user.username,password=old_password) is not None:
            if new_password==confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, "New passwords don't match. Please try again.")
        else:
            messages.error(request, "Incorrect old password. Please try again.")
    
    return render(request,'change_password.html')


def forget_password(request):
    return render(request,'forget_password.html')

def forgot_password_action(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with the given email does not exist.')
            return render(request, 'forget_password.html')

        request.session['id'] = user_obj.id
        request.session['email'] = email
        send_otp(request)
        print(send_otp)
        return redirect('forget_otp')

    return render(request, 'forget_password.html')

def forget_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_key = request.session.get('otp_key')
        otp_valid = request.session.get('otp_valid')
        if otp_key and otp_valid is not None:
            valid_otp = datetime.fromisoformat(otp_valid)
            if valid_otp > datetime.now():
                totp = pyotp.TOTP(otp_key, interval=60)
                if totp.verify(otp):
                    return redirect('new_password')
                else:
                    messages.error(request, 'Invalid Otp')
                    return redirect('forget_otp')
            else:
                clear_session(request)
                messages.error(request, 'Otp expired')
                return redirect('log_in')
        else:
            clear_session(request)
            messages.error(request, 'Didnt get any otp')
            return redirect('log_in')
    return render(request, 'forget_otp.html')

def new_password(request):
    if request.method == 'POST':
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if password_1 == password_2:
            id = request.session.get('id')
            user = User.objects.get(id=id)
            hashed_password = make_password(password_1)
            user.password = hashed_password
            user.save()
            print('passwordchanged')
            return redirect('log_in')
    return render(request, 'new_password.html')


def generate_referral_view(request):
    user_detail = User.objects.filter(email, user_id)
    
    # Get user's email and user ID (replace this with your authentication logic)
    email = "example@example.com"
    user_id = 123

    # Generate referral code
    referral_code = Referral.generate_referral_code(email, user_id)

    # Save referral code to the database or use it in any way you need
    # For example:
    # referral_obj = Referral(referral_code=referral_code)
    # referral_obj.save()

    # Pass the referral code to the signup page
    return render(request, 'signup.html', {'referral_code': referral_code})