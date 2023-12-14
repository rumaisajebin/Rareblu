from django.urls import path
from . import views

urlpatterns=[
    
    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_product',views.admin_product,name='admin_product'),
    path('admin_productview/<int:id>/',views.admin_productview,name='admin_productview'),
    path('admin_addproduct',views.admin_addproduct,name='admin_addproduct'), 
    path('addproduct_perform',views.addproduct_perform,name='addproduct_perform'), 
    path('edit_product/<int:id>/',views.edit_product,name='edit_product'), 
    path('edit_productperfom',views.edit_productperfom,name='edit_productperfom'), 
    path('productactive/<int:id>/',views.productactive,name='productactive'), 
    path('productdelete/<int:id>/',views.productdelete,name='productdelete'), 
    
    
                    
    path('category',views.category,name='category'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('categoryactive/<int:id>/',views.categoryactive,name='categoryactive'),
    path('editcategory_action',views.editcategory_action,name='editcategory_action'),
    path('editcategory/<int:id>',views.editcategory,name='editcategory'),


    path('brand',views.brand,name='brand'),
    path('addbrand',views.addbrand,name='addbrand'),
    path('editbrand/<int:id>',views.editbrand,name='editbrand'),
    path('editbrand_action',views.editbrand_action,name='editbrand_action'),
    path('brandactive/<int:id>/',views.brandactive,name='brandactive'),
    
    
    path('coupon',views.coupon,name='coupon'),
    path('addcoupon',views.addcoupon,name='addcoupon'),
    path('edit_coupon/<int:id>/',views.edit_coupon,name='edit_coupon'),
    path('edit_couponaction',views.edit_couponaction,name='edit_couponaction'),
    
    
    path('customer',views.customer,name='customer'),
    path('customeractive/<int:id>/',views.customeractive,name='customeractive'),
    
    
    path('order',views.order,name='order'),
    path('order_return/<int:order_id>/',views.order_return,name='order_return'),
    path('order_view/<int:order_id>/',views.order_view,name='order_view'),
    path('order_update/<int:order_id>/',views.order_update,name='order_update'),
    path('returnedorders',views.returnedorders,name='returnedorders'),
    path('returned_details/<int:id>/',views.returned_details,name='returned_details'),
    # path('returned_orderview/<int:order_id>/',views.returned_orderview,name='returned_orderview'),
    
    path('category_Offer',views.category_Offer,name='category_Offer'),
    path('add_category_Offer',views.add_category_Offer,name='add_category_Offer'),
    
    path('salesreport',views.salesreport,name='salesreport'),
    path('filter_salesreport',views.filter_salesreport,name='filter_salesreport'),
    path('generate_sales_report_pdf',views.generate_sales_report_pdf,name='generate_sales_report_pdf'),

    ]