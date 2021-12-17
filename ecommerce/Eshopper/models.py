from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields.related import ManyToManyField
from django.forms.widgets import SplitHiddenDateTimeWidget
from cart.models import coupon, payment_gateway
from product.models import commoninfo, product, productImage
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class status(models.TextChoices):
    Active   = 'Active', "Active"
    Deactive = 'Deactive','Deactive'

class Social_Register(models.TextChoices):
    Facebook = 'fb', 'Facebook'
    Twitter  = 'Twitter','Twitter'
    Google   = 'Google', 'Google'

class Order_Status(models.TextChoices):
    Pending     =  'P',"Pending"
    Shipped     =  'S','Shipped'
    Delivered   =  'D','Delivered'
    Processing  =  'PR','Processing'


class User(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=100,default='123')
    birth_date = models.DateField(null=True,blank=True,default='2021-01-01')
    status = models.CharField( max_length=15, choices=status.choices)
    fb_token = models.CharField(max_length=100,null=True,blank=True)
    twitter_token = models.CharField(max_length=100,null=True,blank=True)
    google_token = models.CharField(max_length=100,null=True,blank=True)
    registration_method = models.CharField(max_length=20,choices=Social_Register.choices,null=True,blank=True)

    @property   
    def fullname(self):
        return self.first_name + ' ' + self.last_name 
    
    def __str__(self):
        return  str(self.username)


class user_wish_list(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=CASCADE,default=1)
    

class user_address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    zipcode = models.CharField(max_length=45) 

    def __str__(self):
        return (self.address_1)
   
   
    



# change all the status 
class user_order(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,null=True)
    shipping_method = models.IntegerField(null=True)
    AWB_NO = models.CharField(max_length=100)
    product_id = models.ForeignKey(product,on_delete=CASCADE,null=True)
    payment_gateway_id = models.ForeignKey(payment_gateway,on_delete=CASCADE,null=True)
    transaction_id = models.CharField(max_length=100,null=True)
    created_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=Order_Status.choices)
    grand_total = models.FloatField(null=True,blank=True)
    shipping_charges = models.FloatField(default=0)
    coupon_id = models.ForeignKey(coupon,on_delete=CASCADE,null=True)
    billing_address_1 = models.CharField(max_length=100,default='default')
    billing_address_2 = models.CharField(max_length=100,blank=True,null=True)
    billing_city = models.CharField(max_length=45)
    billing_state = models.CharField(max_length=45)
    billing_country = models.CharField(max_length=45)
    billing_zipcode = models.CharField(max_length=45)
    shipping_address_1 = models.CharField(max_length=100,null=True)
    shipping_address_2 = models.CharField(max_length=100,blank=True,null=True)
    shipping_city = models.CharField(max_length=45,null=True)
    shipping_state = models.CharField(max_length=45,null=True)
    shipping_country = models.CharField(max_length=45,null=True)
    shipping_zipcode = models.CharField(max_length=45,null=True)

    def __str__(self):
        return self.user.username

      
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.sub_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
      
    def total_price(self):
        order = self.orderitem_set.all()
        return sum([(item.quantity * item.product_id.price)for item in order])
        
    def set_grand_total(self):
        try:                   
            if self.coupon_id.is_active:
                final_grand_total = ((self.get_cart_total)* (100 - self.coupon_id.percent_off)/100)+self.shipping_charges 
                return final_grand_total
            else:
                final_grand_total = (self.get_cart_total + self.shipping_charges)
                return final_grand_total
        except:
            if self.coupon_id:
                final_grand_total = ((self.get_cart_total)* (100 - self.coupon_id.percent_off)/100)+self.shipping_charges 
                return final_grand_total
            else:
                final_grand_total = (self.get_cart_total + self.shipping_charges)
                return final_grand_total


class coupon_used(models.Model):
    user_id = models.ForeignKey(User,on_delete=CASCADE)       #forigenkey needed
    order_id = models.ForeignKey(user_order,on_delete=CASCADE)
    created_date = models.DateField(auto_now_add=True)
    coupon_id = models.ForeignKey(coupon,on_delete=models.CASCADE) 

    def get_absolute_url(self):
        return (reverse('custom-admin')) 

class OrderItem(models.Model):
    order_id = models.ForeignKey(user_order,on_delete=CASCADE)
    quantity = models.IntegerField(default=1)
    amount  = models.FloatField(null=True,blank=True)
    product_id = models.ForeignKey(product,on_delete=CASCADE,null=True)
    image_id = models.ForeignKey(productImage,on_delete=CASCADE,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.product_id) + ' ' + str(self.quantity)
    
    @property
    def sub_total(self):    
        product_ = self.product_id
        price=product_.checkOffer()                       

        sub_price=(price * self.quantity)
        return sub_price

    @property
    def final_amt(self):
        product_  = self.product_id
        coupon_ = self.order_id
        shipping_charge_ = self.order_id
        shipping_amt_ = shipping_charge_.shipping_charges
        coupon_id= coupon_.coupon_id
        total_ = product_.checkOffer
        
        discount_ = coupon_id.percent_off
        if coupon_id :
            final_total_ = ((self.sub_total - (self.sub_total * (discount_)//100)) + shipping_amt_)
            return final_total_

        else:
            return (self.sub_total + shipping_amt_)

    @property
    def percent_off_value(self):
  
        coupon_ = self.order_id
        
        coupon_id= coupon_.coupon_id
       
        discount_ = coupon_id.percent_off
        if coupon_id :
            percent_val = (self.sub_total * (discount_)//100)
            return percent_val

        else:
            return "NO COUPON USED "
   

class Wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=CASCADE,null=True,blank=True)
    product_id = models.ForeignKey(product,on_delete=CASCADE,null=True,blank=True)


    def __str__(self) :
        return self.user_id

class OrderHistory(models.Model):
    order_item = models.ForeignKey(user_order,on_delete=CASCADE)
    user_id = models.ForeignKey(User,on_delete=CASCADE)
    

    def __str__(self):
        return self.user_id

            

    

    
