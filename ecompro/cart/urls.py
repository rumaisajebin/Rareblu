from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('product',views.product,name='product'),
    path('product_view/<int:id>/',views.product_view,name='product_view'),
    path('search',views.search,name='search'),
    path('price_filter',views.price_filter,name='price_filter'),


    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('hx_menu_cart/', views.hx_menu_cart, name='hx_menu_cart'),
    path('hx_cart_total/', views.hx_cart_total, name='hx_cart_total'),
    path('update_cart/<int:id>/<str:action>/', views.update_cart, name='update_cart'),
    path('remove_item/<int:id>/', views.remove_item, name='remove_item'),
    
 
    
    path('checkout', views.checkout, name='checkout'),
    path('add_address', views.add_address, name='add_address'),
    path('addaddress_perform', views.addaddress_perform, name='addaddress_perform'),
    path('addressview', views.addressview, name='addressview'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('edit_addressperform/<int:id>/', views.edit_addressperform, name='edit_addressperform'),
    path('addressdelete/<int:id>/', views.addressdelete, name='addressdelete'),

    path('place_order', views.place_order, name='place_order'),
    path('success', views.success, name='success'),
    path('success2', views.success2, name='success2'),
    path('paymentsuccessful/<int:address>/', views.paymentsuccessful, name='paymentsuccessful'),
    path('paymentfailed', views.paymentfailed, name='paymentfailed'),

    
    
    path('view_coupons', views.view_coupons , name='view_coupons'),
    path('wallet', views.wallet , name='wallet'),
    

    path('order_listing', views.order_listing , name='order_listing'),
    path('order_detailview/<int:id>/', views.order_detailview , name='order_detailview'),
    path('cancel_order/<int:order_id>/', views.cancel_order , name='cancel_order'),
    path('return_order/<int:order_id>/', views.return_order , name='return_order'),
      
    path('wishlist', views.wishlist , name='wishlist'),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist , name='add_to_wishlist'),
    path('wish_remove/<int:id>/', views.wish_remove , name='wish_remove'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart , name='remove_from_cart'),
    
    
    ]   