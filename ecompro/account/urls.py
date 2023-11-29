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
    
    
    path('edit_profile_action',views.edit_profile_action,name='edit_profile_action'),
    path('profile',views.profile,name='profile'),
    path('editprofile',views.editprofile,name='editprofile'),
    
    ]