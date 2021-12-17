from django.urls import path
from django.urls.conf import include 
from . import views

app_name = 'product' 
urlpatterns=[
    path('',views.product_view,name='product'),
    path('product-detail/<int:id>/',views.detail_view,name='details-view'),

    path('details/',views.product_details,name='details'),
    
   

 ]