from django.shortcuts import redirect, render
from Eshopper.models import *
from product.models import *

# Create your views here.

def product_view (request):
    return render(request,'Eshopper/shop.html')

def detail_view(request,id):
    try:
        product_message_error = None
        customer = request.user
        order , created = user_order.objects.get_or_create(user = customer, status = False)
        items = order.orderitem_set.all()
        print(id)
        if product.objects.filter(id=id):
            product_ = product.objects.filter(id=id)
            #print(product_)

        else:
            product_message_error = "NO PRODUCT FOUND !"
            return redirect('/')
            

        context = {'product':product_,'error':product_message_error,'items':items}
        return render(request,'Eshopper/product-details.html', context)
    except:
        return redirect('/product/details/')


def product_details(request):
  
   
    return render(request,'Eshopper/product-details.html')

