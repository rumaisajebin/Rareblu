from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart_view',views.cart_view,name='cart_view'),
    path('remove_from_cart/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('change_quantity/<str:product_id>/', views.change_quantity, name='change_quantity'),
    path('hx_cart_total', views.hx_cart_total, name='hx_cart_total'),
    
    path('add_address', views.add_address, name='add_address'),
    path('addaddress_perform', views.addaddress_perform, name='addaddress_perform'),
    path('addressview/<int:id>/', views.addressview, name='addressview'),

    
    path('success', views.success, name='success'),
    path('success2', views.success2, name='success2'),
    ]