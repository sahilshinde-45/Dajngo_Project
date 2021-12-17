
from django.db import models
from datetime import datetime,date, tzinfo
from django.forms.widgets import NullBooleanSelect
from django.urls import reverse
from django.conf import settings
from Eshopper.utils import Status
from ckeditor.fields import RichTextField
import dateutil,datetime,pytz
from django.db.models.deletion import CASCADE

# Create your models here.


class commoninfo(models.Model):
    #created_by  = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='%(class)s_created_by_user',on_delete=CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modify_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='%(class)s_modify_by_user',on_delete=CASCADE)
    #modify_by = models.IntegerField()
    modify_date = models.DateField(auto_now_add=True)
    class Meta:
        abstract = True

class Product_Status(models.TextChoices):
    Available = 'A', 'AVAILABLE'
    UN_Available = 'NA','NOT AVAILABLE'

class product(commoninfo):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=45)
    short_description = models.CharField(max_length=100)
    long_description = RichTextField(blank = True , null = True)
    price = models.FloatField()
    special_price = models.FloatField()
    special_price_from = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    special_price_to = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    status = models.CharField(max_length=30,choices=Product_Status.choices)
    quantity = models.IntegerField()
    meta_description = models.TextField(blank=True,null=True)
    meta_keyword = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=30,choices=Product_Status.choices)
    is_feature = models.BooleanField()
    Pro_Image = models.ImageField(upload_to = "my_images",blank = True, null= True)

    def __str__(self) :
        return  self.name
    
    def get_absolute_url(self):
        return (reverse('custom-admin'))              #kuch karna padega

    
    def checkOffer(self):
        now = datetime.datetime.now()
        if self.special_price_from:
            if self.special_price_from < self. special_price_to and now < self.special_price_to.replace(tzinfo=None) and self.special_price_from.replace(tzinfo =None) <= now:
                special_price_offered = self.special_price
                return special_price_offered 
            else:
                price_offered = self.price
                return price_offered 
        else:
            return self.price
            

class productImage(commoninfo):
    product_id = models.ForeignKey(product,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = "my_images")

    def __str__(self):
        return self.image_name

class Category_Status(models.TextChoices):
    Active = 'A', 'Active'
    Not_Active = 'NA','Not Active'

class category(commoninfo):
    name = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self',on_delete=CASCADE,related_name='child',blank=True,null=True)
    status = models.CharField(max_length=20,choices=Category_Status.choices)

    
    
    def __str__(self):
        if self.parent_id:
            return self.parent_id.name + ' - ' + self.name
        else:
            return self.name
    
class product_categories(models.Model):
    product_id  = models.ForeignKey(product,on_delete=CASCADE)
    category_id = models.ForeignKey(category,on_delete=CASCADE)

class product_attribute(commoninfo):
    name = models.CharField(max_length=45)

    def __str__(self) :
        return self.name

class product_attribute_value(commoninfo):
    product_attribute_id = models.ForeignKey(product_attribute,on_delete=CASCADE)
    attribute_value = models.CharField(max_length=100)

    def __str__(self):
        return self.attribute_value

class product_attribute_assoc(models.Model):
    product_id = models.ForeignKey(product,on_delete=CASCADE)
    product_attribute_id = models.ForeignKey(product_attribute,on_delete=CASCADE)
    product_attribute_value_id = models.ForeignKey(product_attribute_value,on_delete=CASCADE)



