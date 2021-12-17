from django import forms
from django.contrib.flatpages.models import FlatPage
from django.db.models import fields
from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import inlineformset_factory
from django.forms.widgets import DateTimeInput, NumberInput
from Eshopper import form
from Eshopper.models import User,coupon_used, user_order, OrderItem, user_wish_list
from cart.models import coupon
from custom_admin import models
from django.contrib.flatpages.forms import FlatpageForm
from custom_admin.models import BannerHomePage, Cms, contactUs, emailTemplate
from product.models import commoninfo,product,productImage,category,product_categories,product_attribute,product_attribute_value,product_attribute_assoc

class UserRegistration(ModelForm):
    class Meta:
        model =  User
        fields = '__all__'
        exclude = []


    
class formproduct(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(formproduct,self).__init__(*args,**kwargs)
        self.fields['long_description'].required = False
        

    class Meta:
        model = product
        fields = '__all__'
        exclude = ['created_by','modify_by']

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control '}),
            'sku' :forms.TextInput(attrs={'class':'form-control '}),
            'long_description': forms.Textarea(attrs={'class':'form-control '}),
            'short_description': forms.TextInput(attrs={'class':'form-control '}),
            'price':forms.NumberInput(attrs={'class':'form-control','style':'width:11%;'}),
            'special_price':forms.NumberInput(attrs={'class':'form-control','style':'width:11%;'}),
            'special_price_from':forms.DateTimeInput(attrs={'type':'date','style':'width:15%;  padding:10px'}),
            'special_price_to': forms.DateTimeInput(attrs={'type':'date','style':'width:15%;  padding:10px; '}),
            'status': forms.Select(attrs={'class':'form-control','style':'width:25%'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control','style':'width:10%'}),
            'meta_description':forms.Textarea(attrs={'class':'form-control'}),
            'meta_keyword':forms.TextInput(attrs={'class':'form-control'}),
            'is_feature':forms.CheckboxInput(),
        }
        

class formproductImage(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(formproductImage,self).__init__(*args,**kwargs)
        self.fields['image_name'].required = True
    class Meta:
        model = productImage
        fields = '__all__'
        exclude = ['created_by','modify_by']
         
        widgets = {
            'product_id':forms.Select(attrs={'class':'form-control required','style':'width:20%'}),
            'image_name':forms.TextInput(attrs={'class':'form-control required','style':'width:30%'}),
            
        }
#class 1st letter caps 
      

class formcategory(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(formcategory,self).__init__(*args,**kwargs)
        self.fields['name'].required = True

    class Meta:
        model = category
        fields = '__all__'
        exclude = ['created_by','modify_by']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control required'}),
            'parent_id':forms.Select(attrs={'class':'form-control required','style':'width:50%'}),
            'status': forms.Select(attrs={'class':'form-control','style':'width:50%'}),
        }

class formProductCategory(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(formProductCategory,self).__init__(*args,**kwargs)
        self.fields['product_id'].required = True
    class Meta:
        model = product_categories
        fields = '__all__'
        exclude = []
        widgets = {
            'product_id' : forms.Select(attrs={'class':'form-control required','style':'width:70%'}),
            'category_id': forms.Select(attrs={'class':'form-control required','style':'width:70%'}),

        }


class formProductAttribute(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(formProductAttribute,self).__init__(*args,**kwargs)
        self.fields['name'].required = True

    class Meta:
        model = product_attribute
        fields = '__all__'
        exclude = ['created_by','modify_by']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control required'}),
        }

class formProductAttributeValue(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(formProductAttributeValue,self).__init__(*args,**kwargs)
        self.fields['attribute_value'].required = True

    class Meta:
        model = product_attribute_value
        fields = '__all__'
        exclude = ['created_by','modify_by']
        widgets = {
            'product_attribute_id': forms.Select(attrs={'class':'form-control ','style':'width:70%'}),
            'attribute_value': forms.TextInput(attrs={'class':'form-control'}),
        }

class formProductAttibuteAssoc(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(formProductAttibuteAssoc,self).__init__(*args,**kwargs)
        self.fields['product_id'].required = True

    class Meta:
        model = product_attribute_assoc
        fields = '__all__'
        exclude = []

        widget = {
            'product_id' : forms.Select(attrs={'class':'form-control','style':'width:40%'}),
            'product_attribute_id':forms.Select(attrs={'class':'form-control ','style':'width:70%'}),
            'product_attribute_value_id':forms.Select(attrs={'class':'form-control ','style':'width:70%'}),
        }



class FormCoupon(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(FormCoupon,self).__init__(*args,**kwargs)
        self.fields['code'].required = True
    class Meta:
        model = coupon
        fields = '__all__'
        exclude = ['created_by','modify_by']
       
        widgets = {
            'code' : forms.TextInput(attrs={'class':'form-control','style':'width:40%'}),
            'percent_off': forms.NumberInput(attrs={'class':'form-control','style':'width:40%'}),
            'no_of_uses': forms.NumberInput(attrs={'class':'form-control','style':'width:40%'}), 
        }


class FormCouponUsed(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(FormCouponUsed,self).__init__(*args,**kwargs)
        self.fields['user_id'].required = True

    class Meta:
        model = coupon_used
        fields = '__all__'
        exclude = ['created_by','modify_by']
        
        widgets = {
            'user_id':forms.Select(attrs={'class':'form-control','style':'width:40%'}),
            'order_id':forms.Select(attrs={'class':'form-control','style':'width:40%'}),
            'created_date': forms.DateTimeInput(attrs={'class':'form-control','style':'width:40%'}),
            'coupon_id':forms.Select(attrs={'class':'form-control','style':'width:40%'}),
        }


class FormOrder(ModelForm):
    class Meta:
        model = user_order
        fields = '__all__'
        exclude = []

class FormOrderDetails(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = []

class FormWhislist(ModelForm):
    class Meta:
        model = user_wish_list
        fields = '__all__'
        exclude = []

class Form_Banner(ModelForm):
    class Meta:
        model = BannerHomePage
        fields = '__all__'
        exclude = ['created_by','modify_by']


class Form_Email(ModelForm):
    required_css_class = 'required'
    def __init__(self,*args,**kwargs):
        super(Form_Email,self).__init__(*args,**kwargs)
        self.fields['title'].required = True
    class Meta:
        model = emailTemplate
        fields = '__all__'
        exclude = ['created_by','modify_by']

        widgets = {
            'title'   : forms.TextInput(attrs={'class':'form-control'}),
            'subject' : forms.TextInput(attrs={'class':'form-control'}),
            'content' : forms.Textarea(attrs={'class':'form-control'}),
        }

class Form_Cms(FlatpageForm):
    required_css_class = 'required'
    class Meta:
        model = Cms
        fields = ['url','title','content','meta_title','meta_description','meta_keywords','sites']
        exclude = ['created_by','modify_by']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control required'}),
            'url': forms.TextInput(attrs={'class': 'form-control required'}),
            'content': forms.Textarea(attrs={'class':'form-control required','id':'summernote'}),
            'meta_description':forms.Textarea(attrs={'class':'form-control'}),
            'meta_title':forms.TextInput(attrs={'class':'form-control'}),
            'meta_keyword':forms.TextInput(attrs={'class':'form-control'}),

        }

class Form_Contact_us(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = contactUs
        fields = '__all__'
        exclude = ['created_by','modify_by','contact_no']

        widgets = {
            'name':forms.TextInput(attrs = {'class':'form-control required'}),
            'email':forms.EmailInput(attrs={'class':'form-control required'}),
            'message':forms.Textarea(attrs={'class':'form-control','id':'summernote'}),
            'note_admin':forms.Textarea(attrs={'class':'form-control','id':'summernote'}),
        }