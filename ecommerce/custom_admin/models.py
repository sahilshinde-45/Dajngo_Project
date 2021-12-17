from django.db import models
from django.forms.widgets import Textarea
from product.models import commoninfo
from ckeditor.fields import RichTextField
from django.contrib.flatpages.models import FlatPage
# Create your models here.


class contactUs(commoninfo):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    contact_no = models.CharField(max_length=45,null=True,blank=True)
    message = models.TextField()
    note_admin = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.name 
    
class emailTemplate(commoninfo):
    title = models.CharField(max_length=45)
    subject = models.CharField(max_length=255)
    content = RichTextField(blank = True , null = True)

    def __str__(self):
        return self.title


class status(models.TextChoices):
    Active   = 'Active', "Active"
    Deactive = 'Deactive','Deactive'

class BannerHomePage(commoninfo):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="my_images")
    status = models.CharField( max_length=15, choices=status.choices)


    def __str__(self):
        return self.name


class Cms (FlatPage,commoninfo):
    meta_title = models.TextField(null= True,blank = True)
    meta_description = models.TextField(null = True ,blank = True)
    meta_keywords =models.TextField(null = True,blank = True)

    def __str__(self):
        return self.title

class Configuration (commoninfo):
    conf_key   = models.CharField(max_length=45) 
    conf_value = models.CharField(max_length=100)
    status = models.CharField(max_length=15 ,choices=status.choices)

    