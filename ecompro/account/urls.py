from django.urls import path
from . import views

urlpatterns=[
    path('sign_up',views.sign_up,name='sign_up'),
    # path('home',views.home,name='home'),
    path('log_in',views.log_in,name='log_in'),
    path('log_in_perform',views.log_in_perform,name='log_in_perform'),
    path('log_out',views.log_out,name='log_out'),
    path('otp_page', views.otp_page, name='otp_page'),
    path('otp',views.otp,name='otp'),
    path('clear_session',views.clear_session,name='clear_session'),
    ]