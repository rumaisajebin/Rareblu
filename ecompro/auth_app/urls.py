from django.urls import path
from . import views

urlpatterns=[
    path('sign_up',views.sign_up,name='sign_up'),
    path('log_in',views.log_in,name='log_in'),
    path('log_in_perform',views.log_in_perform,name='log_in_perform'),
    path('log_out',views.log_out,name='log_out'),
    path('otp_page', views.otp_page, name='otp_page'),
    path('otp',views.otp,name='otp'),
    path('clear_session',views.clear_session,name='clear_session'),
    path('handle_referral',views.handle_referral,name='handle_referral'),
    
    
    path('forget_password',views.forget_password,name='forget_password'),
    path('forgot_password_action',views.forgot_password_action,name='forgot_password_action'),
    path('forget_otp',views.forget_otp,name='forget_otp'),
    path('new_password',views.new_password,name='new_password'),

    
    
    path('edit_profile_action',views.edit_profile_action,name='edit_profile_action'),
    path('profile',views.profile,name='profile'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('change_password',views.change_password,name='change_password'),
    
    
    ]