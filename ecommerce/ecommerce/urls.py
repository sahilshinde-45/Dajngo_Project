"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler400, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


urlpatterns = [
    path('admin/',admin.site.urls),
    path('custom-admin/', include('custom_admin.url')),
    path('' ,include('Eshopper.url')),
    path('product/',include('product.url')),
    path('cart/',include('cart.url')),
    path('accounts/', include('allauth.urls')),
    path('pages/',include('django.contrib.flatpages.urls')),
    path('marketing/',include('marketing.url')),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#handler404 = 'Eshopper.views.page_404'