from django.contrib import admin
from .models import *
from Eshopper.models import *

# Register your models here.
class couponadmin(admin.ModelAdmin):
    model = coupon
    list_display = ['code','percent_off',"created_by","created_date","modify_by","modify_date"]

admin.site.register(coupon,couponadmin)



class paymentadmin(admin.ModelAdmin):
    model = payment_gateway
    list_display = ['name',"created_by","created_date","modify_by","modify_date"]

admin.site.register(payment_gateway,paymentadmin)

admin.site.register(Wishlist)

""" class coupon_usedadmin(admin.ModelAdmin):
    model = coupon_used
    list_display = ['user_id','order_id','created_date','get_coupon_id']

     def get_user_id(self,obj):
        return obj.user_id.id
    get_user_id.admin_order_field = 'user'
    get_user_id.short_description = 'user_id'

    def get_order_id(self,obj):
        return obj.order_id.id
    get_order_id.admin_order_field = 'order'
    get_order_id.short_description = 'order_id' 

    def get_coupon_id(self,obj):
        return obj.coupon_id.id
    get_coupon_id.admin_order_field = 'coupon'
    get_coupon_id.short_description = 'coupon_id'

admin.site.register(coupon_used,coupon_usedadmin) 



class order_details_admin(admin.ModelAdmin):
    model = order_details
    list_display = ['order_id','get_product_id','quantity','amount']

    def get_order_id(self,obj):
        return obj.order_id.id
    get_order_id.admin_order_field = 'order'
    get_order_id.short_description = 'order_id' 

    def get_product_id(self,obj):
        return obj.product.id
    get_product_id.admin_order_field = 'product'
    get_product_id.short_description = 'product_id'

admin.site.register(order_details,order_details_admin)
 """


