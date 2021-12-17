from django.urls import path
from django.urls.conf import include   
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns=[

    path('',views.home,name='home'),
    path('login/',views.log_in,name='login'),
    path('custom-admin/',views.custom_admin,name='custom-admin'),
    path('contactus/',views.contactus,name='contactus'),
    path('logout/',views.log_out,name='logout'),
    path('account/',views.account,name='account'),
    path('password-reset/',
          auth_views.PasswordResetView.as_view(template_name='Registration/password_reset.html'),
          name='password_reset'),

    path('reset_password_sent/',
          auth_views.PasswordResetDoneView.as_view(template_name='Registration/password_email_reset.html'),
          name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='Registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='Registration/password_reset_complete.html'),
         name='password_reset_complete'),
    
    path('category/<int:id>/',views.fetch_By_Category,name='category'),

    path('pages/pages/',views.Pages,name='page'),

    path('activate/<uidb64>/<token>/',VerificationView.as_view(),name='activate'),
   
    
 ]