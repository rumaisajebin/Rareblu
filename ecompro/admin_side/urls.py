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
    
    # path('search',views.search,name='search'),
    ]