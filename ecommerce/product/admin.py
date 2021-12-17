from django.contrib import admin
from django.db import models
from .models import category, product, product_attribute, product_attribute_assoc, product_attribute_value, product_categories, productImage
from django.utils.html import format_html

# Register your models here.
class productadmin(admin.ModelAdmin):
    model = product
    list_display = ('name','price',"is_feature","quantity","created_by","created_date","modify_by","modify_date")


admin.site.register(product,productadmin) 

class productimageadmin(admin.ModelAdmin):
    model = productImage
    list_display = ['get_id','image_name',"photo_tag","created_by","created_date","modify_by","modify_date"]

    def photo_tag(self,obj):
        return format_html(f'<img src = "/media/{obj.image}" style ="height:100px;width:100px">')
 
    def get_id(self,obj):
        return obj.product_id.id
    get_id.admin_order_field = 'product'
    get_id.short_description = 'product_id'

admin.site.register(productImage,productimageadmin)
    
class categoryadmin(admin.ModelAdmin):
    model = category
    list_display = ["parent_id","name","created_by","created_date","modify_by","modify_date"]

admin.site.register(category,categoryadmin)

class product_cat_admin(admin.ModelAdmin):
    model = product_categories
    list_display = ["get_id_pro","get_id_cat"]

    def get_id_pro(self,obj):
        return obj.product_id.id
    get_id_pro.admin_order_field = 'product'
    get_id_pro.short_description = 'product_id'

    def get_id_cat(self,obj):
        return obj.category_id.id
    get_id_cat.admin_order_field = 'category'
    get_id_cat.short_description = 'category_id'

admin.site.register(product_categories,product_cat_admin)

class product_att_admin(admin.ModelAdmin):
    model = product_attribute
    list_display = ['name',"created_by","created_date","modify_by","modify_date"]

admin.site.register(product_attribute,product_att_admin)

class product_att_val_admin(admin.ModelAdmin):
    model = product_attribute_value
    list_display = ['get_id_pro_attri','attribute_value',"created_by","created_date","modify_by","modify_date"]
    def get_id_pro_attri(self,obj):
        return obj.product_attribute_id.id
    get_id_pro_attri.admin_order_field = 'product_attribute'
    get_id_pro_attri.short_description = 'product_attribute_id'

admin.site.register(product_attribute_value,product_att_val_admin)

class product_att_assoc_admin(admin.ModelAdmin):
    model = product_attribute_assoc
    list_display = ['get_id_pro','get_id_pro_attri','get_id_pro_attri_val']

    def get_id_pro_attri(self,obj):
        return obj.product_attribute_id.id
    get_id_pro_attri.admin_order_field = 'product_attribute'
    get_id_pro_attri.short_description = 'product_attribute_id'

    def get_id_pro(self,obj):
        return obj.product_id.id
    get_id_pro.admin_order_field = 'product'
    get_id_pro.short_description = 'product_id'

    def get_id_pro_attri_val(self,obj):
        return obj.product_attribute_value_id.id
    get_id_pro_attri_val.admin_order_field = 'product_attribute_value'
    get_id_pro_attri_val.short_description = 'product_attribute_value_id'

admin.site.register(product_attribute_assoc,product_att_assoc_admin)
