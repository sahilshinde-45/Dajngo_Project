from django.urls import path 
from . import views 
from .views import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'custom-admin'
urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.log_in,name ='login'),
    path('forget_pass/',views.forget_pass,name='forget_pass'),
    path('logout/',views.log_out,name='logout'),

    path('user/',views.adminuser,name='user-view'),
    path('userAddress/',userAddress,name='userAddress'),
    path('detailuser/<int:id>/',views.user_details,name='detailuser'),
    
    path('product/',views.adminproduct,name='product'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('editproduct/<int:pk>/',login_required(updateproduct.as_view(),login_url='custom-admin:login'),name='editproduct'),
    path('deleteproduct/<int:pk>/',login_required(deleteProduct.as_view(),login_url='custom-admin:login'),name='deleteproduct'),

    path('productimage/',views.admin_product_image,name='productimage'),
    path('addproductimage/',views.add_product_image,name='addproductimage'),
    path('editproductimage/<int:pk>/',login_required(updateproductImage.as_view(),login_url='custom-admin:login'),name='editproductimage'),
    path('deleteimage/<int:id>/',views.delete_image,name='deleteimage'),

    path('category/',views.admin_category,name='category'),
    path('addcategory/',views.add_category,name='addcategory'),
    path('editcategory/<int:id>/',views.edit_category,name='editcategory'),
    path('deletecategory/<int:pk>/',login_required(deletecategory.as_view(),login_url='custom-admin:login'),name='deletecategory'),

    path('product-category/',views.admin_product_category,name='product-category'),
    path('addproduct-category/',views.add_product_category,name='addproduct-category'),
    path('editproduct-category/<int:id>/',views.edit_product_category,name='editproduct-category'),
    path('deleteproduct-category/<int:id>',views.delete_product_category,name='deleteproduct-category'),

    path('listproduct-attribute/',views.admin_product_attribute,name='listproduct-attribute'),
    path('addproduct-attribute/',views.add_product_attribute,name='addproduct-attribute'),
    path('editproduct-attribute/<int:id>/',views.edit_product_attribute,name='editproduct-attribute'),
    path('deleteproduct-attribute/<int:pk>/',login_required(deleteProductAttribute.as_view(),login_url='custom-admin:login'),name='deleteproduct-attribute'),

    path('listproduct-attribute-value/',views.admin_product_attribute_value,name='listproduct-attribute-value'),
    path('addproduct-attribute-value/',views.add_product_attribute_value,name='addproduct-attribute-value'),
    path('editproduct-attribute-value/<int:id>/',views.edit_product_attribute_value,name='editproduct-attribute-value'),
    path('deleteproduct-attribute-value/<int:pk>/',login_required(deleteProductAttributeValue.as_view(),login_url='custom-admin:login'),name='deleteproduct-attribute-value'),

    path('listproduct-attribute-value-ass/',views.admin_product_attribute_value_assoc,name='listproduct-attribute-value-ass'),
    path('addproduct-attribute-value-ass/',views.add_product_attribute_value_assoc,name='addproduct-attribute-value-ass'),
    path('editproduct-attribute-value-ass/<int:id>/',views.edit_product_attribute_value_assoc,name='editproduct-attribute-value-ass'),
    path('deleteproduct-attribute-value-ass/<int:pk>/',login_required(deleteProductAttributeAss.as_view(),login_url='custom-admin:login'),name='deleteproduct-attribute-value-ass'),

    path('list-coupon/',views.list_coupon,name='listcoupon'),
    path('add-coupon/',views.add_coupon,name='addcoupon'),
    path('edit-coupon/<int:pk>/',login_required(UpdateCoupon.as_view(),login_url='custom-admin:login'),name='editcoupon'),
    path('delete-coupon/<int:pk>/',login_required(DeleteCoupon.as_view(),login_url='custom-admin:login'),name='deletecoupon'),

    path('list-coupon_used/',views.list_coupon_used,name='listcoupon_used'),
    path('add-coupon_used/',views.add_coupon_used,name='addcoupon_used'),
    path('edit-coupon_used/<int:pk>/',login_required(UpdateCouponUsed.as_view(),login_url='custom-admin:login'),name='editcoupon_used'),
    path('delete-coupon_used/<int:pk>/',login_required(DeleteCouponUsed.as_view(),login_url='custom-admin:login'),name='deletecoupon_used'),

    path('contact/',views.list_contactUs,name='contact'),
    path('editcontact/<int:id>/',views.edit_contact,name= 'editcontact'),

    path('addorder/',views.listorder,name='order'),
    path('vieworder/<int:id>/',views.vieworder,name="vieworder"),

    path('banner/',views.listbanner,name='banner'),
    path('add-banner/',views.addbanner,name='addbanner'),
    path('edit-banner/<int:id>/',views.editbanner,name='editbanner'),
    path('delete-banner/<int:id>/',views.deletebanner,name='deletebanner'),

    path('report/',views.report,name='report'),
    path('sales-report/',views.sales_report,name='salesreport'),
    path('updatevieworder/<int:id>/',views.update_view_order,name='updatevieworder'),

    path('email/',views.email,name='email'),
    path('edit-email/<int:id>/',views.edit_email,name='edit-email'),
    path('add-email/',views.add_email,name='add-email'),
    path('delete/<int:id>/',views.delete_email,name='delete-email'),
    
    path('cms/',views.list_flat_pages,name='cms'),
    path('add-cms/',views.add_flat_page,name='add-cms'),
    path('edit-cms/<int:id>/',views.edit_flat_page,name='edit-cms'),
    path('delete-cms/<int:id>/',views.delete_flat_page,name='delete-cms'),

]