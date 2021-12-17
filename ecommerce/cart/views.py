from decimal import Context
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import JsonResponse
import json
from django.contrib import messages
from product.models import*
from Eshopper.models import*
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
# Create your views here.

 

def cart(request):   #if not authenticated then waht ?
    
    customer = request.user
    if customer.is_authenticated:
        order , created = user_order.objects.get_or_create(user = customer, status = False)
        items = order.orderitem_set.all()
        order_id = user_order.objects.get(id = order.id)
        #this is for cart product count
        if order.set_grand_total()>=500:
            order.shipping_charges = 50
            order.save()
        else:
            order.shipping_charges = 0
            order.save()

        cartotal = order.get_cart_total
        cartitems = order.get_cart_items
        fetch_Coupon_Code = request.GET.get('CouponCode') #fetching Coupon Code from the site
        
    
        
        coupon_code_message = None
        correct_coupon = None

        if fetch_Coupon_Code:
            try:
                correct_coupon =coupon.objects.get(code = fetch_Coupon_Code)
                order_id.coupon_id = correct_coupon
                order_id.save()
                one_less_coupon = correct_coupon.no_of_uses-1  #
                
                if one_less_coupon < 0 :
                    correct_coupon.is_active = False
                    correct_coupon.save() 
                
                correct_coupon.save()
            except:
                coupon_code_message = "INVALID COUPON" 
                order_id.coupon_id = correct_coupon
                order_id.save()

            if correct_coupon:
                coupon_used_ = coupon_used()
                order_id.coupon_id = correct_coupon
                coupon_used_.user_id = customer
                coupon_used_.order_id = order_id
                coupon_used_.coupon_id = correct_coupon
                coupon_used_.save()
                order_id.save()
            
                
        
        else:
            correct_coupon = None

    

        
        
        context = {'items': items,
                'cartitems':cartitems,
                'carttotal':cartotal,
                'order':order,
                'couponCode': correct_coupon,
                'coupon_code_message':coupon_code_message}

        return render(request,'Eshopper/cart.html',context)
    else:
        
        return HttpResponseRedirect('/login/','YOU NEED TO LOGIN FIRST')

def checkout(request):
    
    customer = request.user
    if customer.is_authenticated:
        user_info = User.objects.get(username=request.user)
    

        order , created = user_order.objects.get_or_create(user = customer, status = False)
        items = order.orderitem_set.all()
        cartotal = order.get_cart_total
        cartitems = order.get_cart_items
        order_id = user_order.objects.get(id = order.id)
        order_id.grand_total = order_id.set_grand_total()
        order_id.save()
        
        
        context = {'items': items,
                'cartitems':cartitems,
                'carttotal':cartotal,
                'order':order,
                'user_info': user_info,}
        return render (request,'Eshopper/checkout.html',context)
    else:
       return HttpResponseRedirect('/login/')


    

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(productId)
    print(action)


    customer = request.user
    product_ = product.objects.get(id = productId)
    #print(product_)
    order , created = user_order.objects.get_or_create(user = customer, status = False)

    orderItem,created = OrderItem.objects.get_or_create(order_id = order,product_id = product_)
    #print(orderItem)
    cartitems = order.get_cart_items

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    
    
    orderItem.save()

   
 

    
    return JsonResponse('Item was added', safe=False)

def updateQuantity(request):
    data = json.loads(request.body)
    quantityFieldValue = data['qfv']
    quantityFieldProduct = data['qfp']


    customer = request.user
    order , created = user_order.objects.get_or_create(user = customer, status = False )
    items = order.orderitem_set.all()
   
    
    pro = product.objects.get(name = quantityFieldProduct)
    product_ = OrderItem.objects.get(product_id = pro.id,order_id=order)
    print('hi')
    product_.quantity = quantityFieldValue
    product_.save()
    print('quantity-json',product_.quantity)
   
    
       
    return JsonResponse('Quantity update', safe=False)



def processOrder(request):

    
   # data = json.loads(request.body)
    transaction_id = request.POST.get('transaction_id')
    print(transaction_id)
    total = request.POST.get('total')
    print(total)
    
    method = payment_gateway.objects.all()
    print(method)
    customer = request.user
    order , created = user_order.objects.get_or_create(user = customer, status = False)
    items = order.orderitem_set.all()
    
    total = float(order.set_grand_total())

    order.transaction_id = transaction_id
    if order.transaction_id == None:
        order.payment_gateway_id = method[0]
        order.save()
        
    else:
        order.transaction_id  = transaction_id
        order.payment_gateway_id = method[1]
        order.save()

    if total == float(order.set_grand_total()):
        order.status = True
    
    order.save()
    
    order_ = user_order.objects.get(id = order.id)
    html_content = render_to_string('email/placed_order.html',{'order':order_,'total':total})
    text_content = strip_tags(html_content)
    send_mail(
        'Here are your Order Details',
        text_content,
        settings.EMAIL_HOST_USER ,
        [request.user.email],  #request.user.email
        html_message=html_content,
        fail_silently=False)
    
    send_mail(
        'User Placed Order Details',
        text_content,
        settings.EMAIL_HOST_USER ,
        ['admin@neosoft.com'],
        html_message=html_content,
        fail_silently=False)




    
   
        

    return JsonResponse('Payment complete',safe=False)




def deleteCartItem(request,id):
    
   item = OrderItem.objects.filter(id=id)
   print(item)
   item.delete()
   return redirect('/cart')


def payment(request):
    
    customer = request.user
    order , created = user_order.objects.get_or_create(user = customer, status = False)
    items = order.orderitem_set.all()
    cartotal = order.get_cart_total
    cartitems = order.get_cart_items

    context = {
        'items' : items,
        'carttotal': cartotal,
        'order':order,
        'cartitems':cartitems
    }

    return render(request,'Eshopper/payment.html',context)


def add_To_Wishlist(request):
    try:
        customer = request.user
        
        wishlist_ = Wishlist.objects.filter(user_id = customer).order_by('-id')
     
        context={'wishlist': wishlist_}
        return render(request,'Eshopper/wishlist.html',context)
    except:
        return render(request,'Eshopper/wishlist.html')

def MyOrder(request):
    try:
        customer = request.user
        order = user_order.objects.filter(user_id = customer)
        y = len(order)
        context = {'order_history': order,'y':y}
        return render(request,'Eshopper/MyOrder.html',context)
    except:
        return render(request,'Eshopper/MyOrder.html')




def track_order(request):
    if request.method == 'POST':
        num = request.POST.get('past-order-number')
        try:
            
            fetch_order = user_order.objects.get(id = num,user = request.user)
            
            list_order = user_order.objects.filter(user=request.user)
            x = len(list_order)
            context={'fetch_order':fetch_order,'list_order':list_order,'y':x}
            return render(request,'Eshopper/trackorder.html',context)
        except:
            messages.error(request,"YOU DON'T HAVE ORDER WITH THIS ID." )
            return render(request,'Eshopper/trackorder.html')


    
    return render(request,'Eshopper/trackorder.html')

 

def updatewishlist(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product_ = product.objects.get(id = productId)
    data = {}
    check_wishlist = Wishlist.objects.filter(product_id = product_,user_id = customer).count()
    if check_wishlist > 0:
        data = {
            'bool':False
        }
    else:
        Wishlist_ = Wishlist.objects.create(
    
            product_id = product_,
            user_id = customer
        )
        data = {
            'bool':True
        }


    return JsonResponse(data)


def deletewishlist(request,id):
   wishlist_item = Wishlist.objects.filter(id=id)
  
   wishlist_item.delete()
   return redirect('/cart/wishlist/')


    