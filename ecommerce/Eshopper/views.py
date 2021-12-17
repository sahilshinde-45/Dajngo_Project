from django.shortcuts import redirect, render
from django.contrib.auth import logout,login,authenticate
from Eshopper.form import MyUserCreationForm
from django.contrib import messages
from django.views.generic import View
from .models import *
from django.core.mail import EmailMessage
from custom_admin.models import *
from product.models import *

from .utils import*

from django.core import mail

from django.utils.encoding import force_bytes
from django.utils.http import  urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import  render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags



# Create your views here.

def home(request):
    category_ = category.objects.all()
    banner_ = BannerHomePage.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order , created = user_order.objects.get_or_create(user = customer, status = False)
        
        items = order.orderitem_set.all()
        
    
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0}
        cartitems = order['get_cart_items']
        
    res = product.objects.all()

    return render(request,'Eshopper/index.html',{'res':res,'cartitems':cartitems,'category':category_,'banner':banner_,})

def custom_admin(request):
    return render(request,'custom_admin/product')


def log_in(request):
    customer = request.user
    """  order , created = user_order.objects.get_or_create(user = customer, status = False)
    items = order.orderitem_set.all()
    cartitems = order.get_cart_items """ 
    
    if not customer.is_authenticated:
        login_message_error = None
        if request.method == 'POST':
            if 'loginbtn' in request.POST:
            
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('/') 
                login_message_error = "Username or Password is incorrect !!" 
        
            
        form = MyUserCreationForm()
        if request.method == 'POST':
            if 'signupbtn' in request.POST:
                form = MyUserCreationForm(request.POST)
                if form.is_valid():
                    form.save()
                    user_ = form.cleaned_data.get('username')
                    email_ = form.cleaned_data.get('email')
                    
                    messages.success(request,'Account created successfully ' + user_)
                    
                    connection = mail.get_connection()
                    connection.open()
                    user1 = User.objects.get(username = user_)
                    uidb64 = urlsafe_base64_encode(force_bytes(user1.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate',kwargs={
                                    'uidb64':uidb64,'token':token_generator.make_token(user1)
                    })
                    activate_url = "http://"+domain+link
                    email_subject = 'Activate your account'
                    email_body    =  'Hi '+ user_ + \
                                     ' Please use this link to verify your account\n' + activate_url + \
                                     '\n If you have any questions, please feel free to contact us at info@shoppingcompany.com or by phone at +91 - 22 - 40500699.'
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        settings.EMAIL_HOST_USER ,
                        [email_]
                    )
                    email.send(fail_silently=False)

                    email2_body =   'Hi Admin '+ user_ + \
                                     ' have created a account on the website with email \n' + email_
                    email2 = EmailMessage(
                        "NEW USER CREATED ACCOUNT",
                        email2_body,
                        settings.EMAIL_HOST_USER,
                        ['admin@neosoft.com']

                    )
                    email2.send(fail_silently=False)
                    connection.close()
                    return redirect('/login/')

    else:
        return redirect('/')
            
    context = {'form':form,'login_message_error':login_message_error}
    return render(request,'Eshopper/login.html',context)



def log_out(request):
    logout(request)
    return redirect('/login/')

def page_404(request,exception):
    return render(request,'Eshopper/404.html')

def contactus(request):
    if request.method =="POST":
        contact = contactUs()
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact.name = name
        contact.email = email
        contact.message = message
        contact.created_by = request.user
        contact.modify_by = request.user
        contact.save()

        html_content = render_to_string('email/contact_email.html',{'contact':contact})
        text_content = strip_tags(html_content)
        send_mail(
        'User Contact US info',
        text_content,
        settings.EMAIL_HOST_USER,
        ['admin@neosoft.com'],
        html_message=html_content,
        fail_silently=False)


        return render(request,'Eshopper/contact-us.html',{'name':name})
    else:
        return render(request,'Eshopper/contact-us.html')

def account(request):
   
   
    try:
        customer = request.user
         
        user_address.objects.get_or_create(user = customer)

        order , created = user_order.objects.get_or_create(user = customer, status = False)
        items = order.orderitem_set.all()
        address_info = user_address.objects.get(user = customer)
        print(address_info)
        
       

        user_info = User.objects.get(username = customer)
        print('u',user_info)

        

        if request.method == 'POST':
            addressInf = user_order.objects.filter(user_id = user_info) 
            print(addressInf)
            for x in addressInf:
                
                addressInfo = x
                
            print(addressInfo)
            fetch_address1 = request.POST.get('address1')
          
            fetch_address2 = request.POST.get('address2')
            fetch_mobile_Number = request.POST.get('number')
            fetch_country = request.POST.get('country')
            fetch_state = request.POST.get('state')
            fetch_city = request.POST.get('city')
            fetch_zipcode = request.POST.get('postcode')
            fetch_email = request.POST.get('ship_email')
            print(fetch_email)
          

            addressInfo.shipping_address_1 = fetch_address1
            addressInfo.shipping_address_2 = fetch_address2
            addressInfo.shipping_country   = fetch_country
            addressInfo.shipping_state     = fetch_state
            addressInfo.shipping_city      = fetch_city
            addressInfo.shipping_zipcode   = fetch_zipcode
            user_info.phone_number         = fetch_mobile_Number
            user_info.email                = fetch_email
            addressInfo.save()
            user_info.save()

            
            
            messages.success(request,"INFORMATION ADDED SUCCESSFULLY")
        
       
            #addressInfo = user_order.objects.get(user_id = user_info)
            fetch_billing_address1 = request.POST.get('billing_address1')
            fetch_billing_address2 = request.POST.get('billing_address2')
            fetch_billing_country = request.POST.get('billing_country')
            fetch_billing_state = request.POST.get('billing_state')
            fetch_billing_city = request.POST.get('billing_city')
            fetch_billing_postcode = request.POST.get('billing_postcode')
            
            addressInfo.billing_address_1 = fetch_billing_address1
            addressInfo.billing_address_2 = fetch_billing_address2
            addressInfo.billing_country   = fetch_billing_country
            addressInfo.billing_state     = fetch_billing_state
            addressInfo.billing_city      = fetch_billing_city
            addressInfo.billing_zipcode  = fetch_billing_postcode
            addressInfo.save()


            #info user_addres
            
            address_info.address_1 = fetch_billing_address1
            print(address_info.address_1)
            address_info.address_2 = fetch_billing_address2
            address_info.country  =  fetch_billing_country
            address_info.state   =   fetch_billing_state
            address_info.city    =   fetch_billing_city
            address_info.zipcode  =  fetch_billing_postcode
            address_info.save()   
            

            


            return redirect('/cart/checkout/')



        context = {
            'items':items,
            'order':order,
            'user_info':user_info,
            
        }
        return render(request,'Eshopper/account.html',context)
    except:
        return render(request,'Eshopper/account.html')



def fetch_By_Category(request,id):

    customer = request.user
    if customer.is_authenticated:
        fetch_cat = product_categories.objects.filter(category_id=id)
        order , created = user_order.objects.get_or_create(user = customer, status = False)
            
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items


        context ={ 'fetch_cat' : fetch_cat,
                'cartitems' : cartitems,
                
                }
    else:
        fetch_cat = product_categories.objects.filter(category_id=id)
        context = {'fetch_cat': fetch_cat}
        return render(request,'Eshopper/category.html',context)

    return render(request,'Eshopper/category.html',context)

def Pages(request):
    return render(request,'flatpages/default.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        return redirect('/')
