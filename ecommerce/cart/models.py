from datetime import tzinfo
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse

from product.models import commoninfo

# Create your models here.

class coupon(commoninfo):
    code  = models.CharField(max_length=45,null=True)
    percent_off = models.FloatField()
    no_of_uses = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self) :
        return self.code 

    def get_absolute_url(self):
        return (reverse('custom-admin')) 

""" class coupon_used(models.Model):
    user_id = models.ForeignKey(User,on_delete=CASCADE)       #forigenkey needed
    order_id = models.ForeignKey(user_order,on_delete=CASCADE)
    created_date = models.DateField(auto_now_add=True)
    coupon_id = models.ForeignKey(coupon,on_delete=models.CASCADE)  """

class payment_gateway(commoninfo):
    name = models.CharField(max_length=45)

    def __str__(self) :
        return self.name



""" class order_details(models.Model):
    order_id = models.ForeignKey(user_order,on_delete=CASCADE)
    quantity = models.IntegerField()
    amount  = models.FloatField()
    product = models.ForeignKey(product,on_delete=CASCADE) """
