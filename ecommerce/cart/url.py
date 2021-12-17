from django.urls import path
from . import views


urlpatterns=[
    path('',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('updateitem/',views.updateItem,name='updateitem'),
    path('updatequantity/',views.updateQuantity,name='updatequantity'),
    path('processOrder/',views.processOrder,name='processOrder'),
    path('deletecartitem/<int:id>/',views.deleteCartItem,name='deletecartitem'),
    path('payment/',views.payment,name='payment'),
    path('wishlist/',views.add_To_Wishlist,name='wishlist'),
    path('updatewishlist/',views.updatewishlist,name='updatewishlist'),
    path('deletewishlist/<int:id>/',views.deletewishlist,name='deletewishlist'),
    path('trackorder/',views.track_order,name='trackorder'),
    path('myorder/',views.MyOrder,name='myorder'),
    

]