from django.contrib import admin
from django.db import models
from django.db.models import fields
from .models import OrderHistory, User,user_address, user_order,user_wish_list,coupon_used,OrderItem
from django.contrib.auth.admin import UserAdmin
from product.models import product
#from .form import MyUserCreationForm
# Register your models here.


class userAdmin(UserAdmin):
    model = User
    list_display=['username','email','first_name','last_name','phone_number','is_staff']

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Extra Info',
            {
                'fields':(
                    'phone_number',
                    'birth_date',
                    'registration_method',
                    'status',
                    
                )
            }
        )
    )
    #add_form = MyUserCreationForm
class userWishlist(admin.ModelAdmin):
    model = product
    list_display = ['get_user_id','product']

    def get_user_id(self,obj):
        return obj.user.id
    
    get_user_id.admin_order_field = 'user'
    get_user_id.short_description = 'user_id'

    def get_id_pro(self,obj):
        return obj.product.id
    get_id_pro.admin_order_field = 'product'
    get_id_pro.short_description = 'product_id'



    
class userAddress(admin.ModelAdmin):
    model = user_address
    list_display=('get_name','address_1','zipcode')
    def get_name (self,obj):
        return obj.user.username
    
    get_name.admin_order_field = 'user'
    get_name.short_description = 'username'


class userorder_admin(admin.ModelAdmin):
    model = user_order
    list_display = ['get_user_id','get_payment_id','get_coupon_id','transaction_id','grand_total','shipping_address_1']
    def get_user_id(self,obj):
        return obj.user
    get_user_id.admin_order_field = 'user'
    get_user_id.short_description = 'user_id'
    def get_payment_id(self,obj):
        return obj.payment_gateway_id
    get_payment_id.admin_order_field = 'payment_gateway'
    get_payment_id.short_description = 'payment_gateway_id'
    def get_coupon_id(self,obj):
        return obj.coupon_id
    get_coupon_id.admin_order_field = 'coupon'
    get_coupon_id.short_description = 'coupon_id'

class coupon_usedadmin(admin.ModelAdmin):
    model = coupon_used
    list_display = ['get_user_id','get_order_id','created_date','get_coupon_id']

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
    model = OrderItem
    list_display = ['get_order_id','get_product_id','quantity','amount']

    def get_order_id(self,obj):
        return obj.order_id.id
    get_order_id.admin_order_field = 'order'
    get_order_id.short_description = 'order_id'

    def get_product_id(self,obj):
        return obj.product_id.id
    get_product_id.admin_order_field = 'product'
    get_product_id.short_description = 'product_id'

admin.site.register(OrderItem,order_details_admin)

class product():
    pass
admin.site.register(User,userAdmin)
admin.site.register(user_wish_list,userWishlist)
admin.site.register(user_address,userAddress)
admin.site.register(user_order,userorder_admin)

admin.site.register(OrderHistory)