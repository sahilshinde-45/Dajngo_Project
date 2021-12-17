import json
from django import http
from django.contrib.messages.api import success
from django.db import models
from django.db.models.expressions import F, OrderBy
from django.forms import inlineformset_factory
from django.http import request
from django.http.response import Http404, HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import get_list_or_404, render,redirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import UpdateView,DeleteView,ListView,CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from .models import BannerHomePage, Cms, contactUs
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from cart.models import coupon
from .form import *
from Eshopper.models import User, coupon_used, user_address,user_wish_list,OrderItem,user_order
from product.models import category, product, product_attribute, product_attribute_assoc, product_attribute_value, product_categories, productImage
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout 
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import get_template, render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags

# Create your views here.
@login_required(login_url='custom-admin:login')
def home(request):
    res = User.objects.all().count()
    res_pro = product.objects.all().count()
    res_coup = coupon.objects.all().count()
    return render(request,'custom_admin/index.html',{'res':res,'res_pro':res_pro,'res_coup':res_coup})

def log_in(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request,data = request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(request,username = uname,password = upass)
                if user is not None:
                    login(request,user)
                    return redirect("custom-admin:home")
            else:
                messages.error(request,"THIS IS A ERROR")
                return redirect("custom-admin:login")
        
        else:
            fm = AuthenticationForm()
            return render(request,'custom_admin/login.html',{'form':fm})
    else:
        return redirect('custom-admin:home')

def forget_pass(request):
    return render(request,'custom_admin/forget_pass.html')

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('custom-admin:login'))


@login_required(login_url='custom-admin:login')
def adminuser(request):
    res = User.objects.all()
    
    return render(request,'custom_admin/user.html',{'res':res})

@login_required(login_url='custom-admin:login')
def user_details(request,id):
    details = User.objects.get(id=id)
    return render(request,'custom_admin/detailuser.html',{'details':details})



@login_required(login_url='custom-admin:login')
def userAddress(request):
    res = user_address.objects.all()
    return render(request,'custom_admin/userAddress.html',{'res':res})



@login_required(login_url='custom-admin:login')
def adminproduct(request):
    res = product.objects.all()
    
    return render(request,'custom_admin/product.html',{'res':res})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_product',login_url='custom-admin:login')
def addproduct(request):
    if request.method == "POST":
        fm = formproduct(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
            return HttpResponseRedirect('/custom-admin/product/')
        else:
            messages.error(request,'ERROR WHILE FILLING THE FORM')
    else:
        fm = formproduct()
    return render(request,'custom_admin/addproduct.html',{'form':fm})


class updateproduct(PermissionRequiredMixin,UpdateView):
    permission_required = 'custom_admin.change_product'
    
    model = product
    form_class = formproduct 
    template_name= 'custom_admin/editproduct.html'
    login_url = 'custom-admin:login'

    def dispatch(self, request, *args, **kwargs):
        Category_Formset = inlineformset_factory(product,
                                                product_categories,
                                                form=formProductCategory,
                                                
                                                extra=1,can_delete=False
        )
        Attribute_Formset = inlineformset_factory(product,
                                                product_attribute_assoc,
                                                form = formProductAttibuteAssoc,
                                                extra=1,can_delete=False

        )
        Image_Formset = inlineformset_factory(product,
                                            productImage,
                                            fields = ['image_name','image'],
                                            extra=1,can_delete=False
        )

        self.Product = self.get_object()
        self.Category_Formset = Category_Formset
        self.Attribute_Formset = Attribute_Formset
        self.Image_formset = Image_Formset

        #for template
        self.Category_formset = Category_Formset(instance=self.Product)
        self.Attribute_formset = Attribute_Formset(instance=self.Product)
        self.Image_Formset = Image_Formset(instance=self.Product)
      
        return super(updateproduct,self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        Category_Formset = self.Category_Formset(self.request.POST,instance=self.Product)
        attribute_Formset = self.Attribute_Formset(self.request.POST,instance=self.Product)
        Image_Formset = self.Image_formset(self.request.POST,self.request.FILES,instance=self.Product)
       # print(self.request.POST)
       # print(Image_Formset)
        if Category_Formset.is_valid() and attribute_Formset.is_valid() and Image_Formset.is_valid():

            Category_Formset.save()
            attribute_Formset.save()
            #print('hi')
            Image_Formset.save()
            #print('bye')
            
        

        return super(updateproduct,self).form_valid(form)
    
    def post(self,request,**kwargs):

        try:
            if request.POST.get('data') == 'Category':
                v = request.POST.get('value')
                product_categories.objects.filter(id=v).delete()
                return HttpResponseRedirect('/custom-admin/editproduct/{}/'.format(self.kwargs['pk'])) 

            if request.POST.get('data') == 'Attribute':
                v = request.POST.get('value')
                product_attribute_assoc.objects.filter(id=v).delete()
                return HttpResponseRedirect('/custom-admin/editproduct/{}/'.format(self.kwargs['pk']))

            if request.POST.get('data') == 'Image':
                v = request.POST.get('value')
                productImage.objects.get(id=v).delete()
                return HttpResponseRedirect('/custom-admin/editproduct/{}/'.format(self.kwargs['pk']))
            return super(updateproduct,self).post(request,**kwargs)
        except Exception as e:
            return HttpResponseRedirect('/custom-admin/editproduct/{}/'.format(self.kwargs['pk']))

        
    def get_context_data(self, **kwargs):
        context = super(updateproduct, self).get_context_data(**kwargs)
        context['Category_Formset'] = self.Category_formset
        context['attribute_Formset'] = self.Attribute_formset
        context['Image_formset']  = self.Image_Formset


        return context
        
    

class deleteProduct(PermissionRequiredMixin,DeleteView):
    permission_required = 'custom_admin.delete_product'
    model = product
    template_name = 'custom_admin/delete_product.html'
    success_url = reverse_lazy('custom-admin')


    
@login_required(login_url='custom-admin:login')
def admin_product_image(request):
    res = productImage.objects.all()
    return render(request,'custom_admin/list_product_image.html',{'res':res})  

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_productImage',login_url='custom-admin:login')
def add_product_image(request):

    if request.method == 'POST':
        #import pdb;pdb.set_trace()

        fm = formproductImage(request.POST,request.FILES)
        if fm.is_valid():
            messages.success(request,'IMAGE UPLOADED SUCCESSFULLY')  
            
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
            HttpResponseRedirect('/custom-admin/productimage/') 
        else:
            messages.error(request,'error')
    else:
        fm = formproductImage()
   
    return render(request,'custom_admin/add_product_image.html',{'form':fm}) 


 
class updateproductImage(PermissionRequiredMixin,UpdateView):
    permission_required = 'custom_admin.change_productImage'
    model = productImage
    template_name= 'custom_admin/edit_product_image.html'
    form_class = formproductImage


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_productImage',login_url='custom-admin:login')
def delete_image(request,id):
    res = productImage.objects.get(id=id)
    if request.method == "POST":
        res.delete()
        return redirect('/custom-admin/productimage/')
    
    context = {'res':res}
    return render(request,'custom_admin/delete_product_Image.html',context)


@login_required(login_url='custom-admin:login')
def admin_category(request):
    res  = category.objects.all()
    return render(request,'custom_admin/list_category.html',{'res':res})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_category',login_url='custom-admin:login')
def add_category(request):
    if request.method == "POST":
        fm = formcategory(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
            return redirect('/custom-admin/category')

        else:
            messages.error(request,"ERROR WHILE FILLING FORM")
    else:
        fm = formcategory()
    return render(request,'custom_admin/add_category.html',{'form':fm})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_category',login_url='custom-admin:login')
def edit_category(request,id):
    res = category.objects.get(id=id)
    form = formcategory(instance=res)

    if request.method == 'POST':
        form = formcategory(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('/custom-admin/category')
    return render(request,'custom_admin/edit_category.html',{'form':form})


class deletecategory(PermissionRequiredMixin,DeleteView):
    permission_required = 'custom_admin.delete_category'
    model = category
    template_name = 'custom_admin/delete_category.html'
    fields = '__all__'
    success_url = reverse_lazy('custom-admin')





@login_required(login_url='custom-admin:login')
def admin_product_category(request):
    res = product_categories.objects.all()
    return render(request,'custom_admin/list_product_category.html',{'res':res})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_product_categories',login_url='custom-admin:login')  
def add_product_category(request):
    if request.method == "POST":
        fm = formProductCategory(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
            return redirect('/custom-admin/product-category')

        else:
            messages.error(request,"ERROR WHILE FILLING FORM")
    else:
        fm = formProductCategory()
    return render(request,'custom_admin/add_product_category.html',{'form':fm})
    

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_product_categories',login_url='custom-admin:login')
def edit_product_category(request,id):
    res = product_categories.objects.get(id=id)
    form = formProductCategory(instance=res)

    if request.method == 'POST':
        form = formProductCategory(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('/custom-admin/product-category')
    return render(request,'custom_admin/edit_product_category.html',{'form':form})



@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.delete_product_categories',login_url='custom-admin:login')
def delete_product_category(request,id):
    res = product_categories.objects.get(id=id)
    if request.method == "POST":
        res.delete()
        return redirect('/custom-admin/product-category')
    
    context = {'res':res}
    return render(request,'custom_admin/delete_product_category.html',context)

@login_required(login_url='custom-admin:login')
def admin_product_attribute(request):
    res = product_attribute.objects.all()
    return render(request,'custom_admin/list_product_attribute.html',{'res':res})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_product_attribute',login_url='custom-admin:login')
def add_product_attribute(request):
    if request.method == "POST":
        fm = formProductAttribute(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
            return redirect('/custom-admin/listproduct-attribute')
        else:
            messages.error(request,'ERROR WHILE FILLING FORM ')
    else:
        fm = formProductAttribute()
    return render(request,'custom_admin/add_product_attribute.html',{'form':fm})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_product_attribute',login_url='custom-admin:login')
def edit_product_attribute(request,id):
    
    res = product_attribute.objects.get(id=id)
    form = formProductAttribute(instance=res)

    if request.method == 'POST':
        form = formProductAttribute(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('/custom-admin/product-category')
    
    return render(request,'custom_admin/edit_product_attribute.html',{'form':form})



class deleteProductAttribute(PermissionRequiredMixin,DeleteView):
    permission_required = 'custom_admin.delete_product_attribute'
    model = product_attribute
    template_name = 'custom_admin/delete_product_attribute.html'
    success_url = reverse_lazy('custom-admin')


@login_required(login_url='custom-admin:login')
def admin_product_attribute_value(request):
    res = product_attribute_value.objects.all()
    return render(request,'custom_admin/list_pro_attri_val.html',{'res':res})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_product_attribute_value',login_url='custom-admin:login')
def add_product_attribute_value(request):
    if request.method == "POST":
        fm = formProductAttributeValue(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
        else:
            messages.error(request,'ERROR WHILE FILLING FORM ')
    else:
        fm = formProductAttributeValue()
    return render(request,'custom_admin/add_pro_attri_val.html',{'form':fm})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_product_attribute_value',login_url='custom-admin:login')
def edit_product_attribute_value(request,id):
    
    res = product_attribute_value.objects.get(id=id)
    form = formProductAttributeValue(instance=res)

    if request.method == 'POST':
        form = formProductAttributeValue(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('/custom-admin/product-category')
    
    return render(request,'custom_admin/edit_pro_attri_val.html',{'form':form})
    



class deleteProductAttributeValue(PermissionRequiredMixin,DeleteView):
    permission_required = 'custom_admin.delete_product_attribute_value'
    model = product_attribute_value
    template_name = 'custom_admin/delete_product_attribute_value.html'
    success_url = reverse_lazy('custom-admin')


@login_required(login_url='custom-admin:login')
def admin_product_attribute_value_assoc(request):
    res = product_attribute_assoc.objects.all()
    return render(request,'custom_admin/list_pro_attri_val_ass.html',{'res':res})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_product_attribute_assoc',login_url='custom-admin:login')
def add_product_attribute_value_assoc(request):
    if request.method == "POST":
        fm = formProductAttibuteAssoc(request.POST)
        if fm.is_valid():
            
            fm.save()
        else:
            messages.error(request,'ERROR WHILE FILLING FORM ')
    else:
        fm = formProductAttibuteAssoc()
    return render(request,'custom_admin/add_pro_attri_val_ass.html',{'form':fm})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_product_attribute_assoc',login_url='custom-admin:login')
def edit_product_attribute_value_assoc(request,id):
    res = product_attribute_assoc.objects.get(id=id)
    form = formProductAttibuteAssoc(instance=res)

    if request.method == 'POST':
        form = formProductAttibuteAssoc(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('/custom-admin/product-listproduct-attribute-value/')
    
    return render(request,'custom_admin/edit_pro_attri_val_ass.html',{'form':form})


class deleteProductAttributeAss(PermissionRequiredMixin,DeleteView):
    permission_required='custom_admin.delete_product_attribute_assoc'
    model = product_attribute_assoc
    template_name = 'custom_admin/delete_product_attribute_ass.html'
    success_url = reverse_lazy('custom-admin')

@login_required(login_url='custom-admin:login')
def list_coupon(request):
    res = coupon.objects.all()
    return render(request,'coupons/list_coupon.html',{'res':res})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_coupon',login_url='custom-admin:login')
def add_coupon(request):
    if request.method == "POST":
        fm = FormCoupon(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
        else:
            messages.error(request,'ERROR WHILE FILLING FORM ')
    else:
        fm = FormCoupon()
    return render(request,'coupons/add_coupon.html',{'form':fm})



class UpdateCoupon(PermissionRequiredMixin,UpdateView):
    permission_required = 'custom_admin.change_coupon'
    model = coupon
    template_name= 'coupons/edit_coupon.html'
    form_class = FormCoupon



class DeleteCoupon(PermissionRequiredMixin,DeleteView):
    permission_required = 'custom_admin.delete_coupon'
    model = coupon
    template_name = 'coupons/delete_coupon.html'
    success_url = reverse_lazy('custom-admin')

@login_required(login_url='custom-admin:login')
def list_coupon_used(request):
    res = coupon_used.objects.all()
    return render(request,'coupons/list_coupon_used.html',{'res':res})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_coupon_used',login_url='custom-admin:login')
def add_coupon_used(request):
    if request.method == "POST":
        fm = FormCouponUsed(request.POST)
        if fm.is_valid():
            fm.save()
        else:
            messages.error(request,'ERROR WHILE FILLING FORM ')
    else:
        fm = FormCouponUsed()
    return render(request,'coupons/add_coupon_used.html',{'form':fm})



class UpdateCouponUsed(PermissionRequiredMixin,UpdateView):
    permission_required = 'custom_admin.change_coupon_used'
    model = coupon_used
    template_name= 'coupons/edit_coupon_used.html'
    form_class = FormCouponUsed


class DeleteCouponUsed(PermissionRequiredMixin,DeleteView):
    permission_required = 'custom_admin.delete_coupon_used'
    model = coupon_used
    template_name = 'coupons/delete_coupon_used.html'
    success_url = reverse_lazy('custom-admin')

@login_required(login_url='custom-admin:login')
def list_contactUs(request):
    res = contactUs.objects.all()
    return render(request,'contact/contact.html',{'res':res})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_contactUs',login_url='custom-admin:login')
def edit_contact(request,id):
    res = contactUs.objects.get(id=id)
    form = Form_Contact_us(instance=res)

    if request.method == 'POST':
        form = Form_Contact_us(request.POST,instance=res)
        if form.is_valid():
            form.save()
            

            res_ = contactUs.objects.get(id =id)
            html_content = render_to_string('email/admin_reply_contact.html',{'res':res_})
            text_content = strip_tags(html_content)
            send_mail(
            'Reply to your query',
            text_content,
            'noreply@gmail.com',
            [res_.email],
            html_message=html_content,
            fail_silently=False)
            return redirect('/custom-admin/contact')
        
    return render(request,'contact/edit_contact.html',{'form':form})


@login_required(login_url='custom-admin:login')
def listorder(request):
    res = user_order.objects.select_related('user','payment_gateway_id').prefetch_related('orderitem_set__product_id').all()
    for order in res:
        order.set_grand_total()
    return render(request,'order/order.html',{'res':list(res)})


@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.view_user_order',login_url='custom-admin:login')
def vieworder(request,id):

    try:
        order_detail = user_order.objects.select_related('user','payment_gateway_id').prefetch_related('orderitem_set__product_id').get(id=id)
        total=order_detail.set_grand_total()
    except user_order.DoesNotExist:
        return HttpResponse("The Order Does not Exists!")
    return render(request,'order/vieworder.html',{'order_detail': order_detail,'total':total})

def update_view_order(request,id):
        if request.method == "POST":
            data = json.loads(request.body)
            selected_status = data['select_status']
            print(selected_status)
            order_detail =   order_detail = user_order.objects.select_related('user','payment_gateway_id').prefetch_related('orderitem_set__product_id').get(id=id)

            order_detail.status = selected_status
            order_detail.save()
            return JsonResponse('selected item',safe=False)
  


@login_required(login_url='custom-admin:login')
def listbanner(request):
    res = BannerHomePage.objects.all()
    return render(request,'custom_admin/banner.html',{'res':res})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_BannerHomePage',login_url='custom-admin:login')
def addbanner(request):
    if request.method == "POST":
        fm = Form_Banner(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
            return redirect('/custom-admin/banner')

        else:
            messages.error(request,"ERROR WHILE FILLING FORM")
    else:
        fm = Form_Banner()
    return render(request,'custom_admin/add_banner.html',{'form':fm})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_BannerHomePage',login_url='custom-admin:login')
def editbanner(request,id):
    res = BannerHomePage.objects.get(id=id)
    form = Form_Banner(instance=res)

    if request.method == 'POST':
        form = Form_Banner(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('/custom-admin/banner')
    return render(request,'custom_admin/edit_banner.html',{'form':form})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.delete_BannerHomePage',login_url='custom-admin:login')
def deletebanner(request,id):
    res = BannerHomePage.objects.get(id=id)
    if request.method == "POST":
        res.delete()
        return redirect('/custom-admin/banner')
    
    context = {'res':res}
    return render(request,'custom_admin/delete_banner.html',context)

@login_required(login_url='custom-admin:login')
def report(request):
    if request.method == "GET":
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                obj = User.objects.values().all()
                print()
                context = {
                    "data": [data for data in obj],
                }
                
                return JsonResponse(context)

    if request.method == "POST":
        data = json.loads(request.body)
        selected_option = data['selected_option']
        if selected_option == 'coupon':
            coupon_report = coupon.objects.values().all()
             
            context = {'data':[data for data in coupon_report], 
            'columns':[
                {'title':"ID",'data' : "id" },
                {'title':"Created By",'data' :  "created_by_id"},
                {'title':"Modify By",'data' :  "modify_by_id" },
                {'title':"Code",'data' :  "code" },
                {'title':"Percent off",'data' : "percent_off"},
                
            ]
            }
            return JsonResponse(context,safe=False)
        elif selected_option == 'user':
            user_report = User.objects.values().all()
             
            context = {'data':[data for data in user_report], 
            "columns": [
                    {'title':'ID','data': 'id' },
                    {'title':'Date Joined','data': "date_joined" },
                    {'title':'Active','data': "is_active" },
                    {'title':'User','data': "username" },
                    {'title':'Email','data': "email" },
                
                ]
            }
            return JsonResponse(context,safe=False)

    return render(request,'order/report.html')

@login_required(login_url='custom-admin:login')
def sales_report(request):    
    
    if request.method == 'POST':
        data = json.loads(request.body)
        fetch_from_date = data['from']
        fetch_to_date = data['to']
        print('f',fetch_from_date)
        print('t',fetch_to_date)
    
   
        
        order_table = user_order.objects.filter(created_date__gte=fetch_from_date , created_date__lte=fetch_to_date).values()
        print(order_table)
        context={'data':[data for data in order_table],
        "columns": [
            {'title':'ID','data': 'id' },
            {'title':'user name','data': "user_id" },
            {'title':'Payment Method','data': "payment_gateway_id_id" },
            {'title':'Transaction ID','data': "transaction_id" },
            
            {'title':'Created Date','data': "created_date" },
            ]
        }

        return JsonResponse(context,safe=False)
        
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        
        order_table = user_order.objects.values().all()
        print(order_table)
        context={'data':[data for data in order_table],
        }

        return JsonResponse(context,safe=False)
  
    return render(request,'order/salesreport.html')


@login_required(login_url='custom-admin:login')
def email(request):
    res = emailTemplate.objects.all()
    return render(request,'contact/email.html',{'res':res})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_emailTemplate',login_url='custom-admin:login')
def add_email(request):
    if request.method == "POST":
        fm = Form_Email(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.save()
            return redirect('/custom-admin/email')

        else:
            messages.error(request,"ERROR WHILE FILLING FORM")
    else:
        fm = Form_Email()
    return render(request,'contact/add_email.html',{'form':fm})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_emailTemplate',login_url='custom-admin:login')
def edit_email(request,id):
    res = emailTemplate.objects.get(id=id)
    form = Form_Email(instance=res)

    if request.method == 'POST':
        form = Form_Email(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('/custom-admin/email')
    return render(request,'contact/edit_email.html',{'form':form})

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.delete_emailTemplate',login_url='custom-admin:login')
def delete_email(request,id):
    res = emailTemplate.objects.get(id=id)
    if request.method == "POST":
        res.delete()
        return redirect('/custom-admin/email')
    
    context = {'res':res}
    
    return render(request,'contact/delete_email.html',context)  
    
@login_required(login_url='custom-admin:login')
def list_flat_pages(request):
    res = Cms.objects.all()
    context={'res':res}
    return render(request,'custom_admin/flatpage.html',context)

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.add_Cms',login_url='custom-admin:login')
def add_flat_page(request):
    if request.method == "POST":
        fm = Form_Cms(request.POST)
        if fm.is_valid():
            fm.instance.created_by = request.user
            fm.instance.modify_by = request.user
            fm.instance.template_name = 'Eshopper/flatpages/default.html'
            fm.save()
            return redirect('/custom-admin/cms')

        else:
            messages.error(request,"ERROR WHILE FILLING FORM")
    else:
        fm = Form_Cms()
    

    context={'form':fm}
    return render(request,'custom_admin/add_flat_page.html',context)

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.change_Cms',login_url='custom-admin:login')
def edit_flat_page(request,id):
    res = Cms.objects.get(id=id)
    form = Form_Cms(instance=res)

    if request.method == 'POST':
        form = Form_Cms(request.POST,instance=res)
        if form.is_valid():
            form.save()
            return redirect('/custom-admin/cms')
   
    context={'form':form}
    return render(request,'custom_admin/edit_flat_page.html',context)

@login_required(login_url='custom-admin:login')
@permission_required('custom_admin.delete_Cms',login_url='custom-admin:login')
def delete_flat_page(request,id):
    res = Cms.objects.get(id=id)
    if request.method == "POST":
        res.delete()
        return redirect('/custom-admin/cms')
    
    context = {'res':res}
    
        
    return render(request,'custom_admin/delete_flat_page.html',context)
            
      

   




