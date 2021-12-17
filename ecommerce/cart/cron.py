from django.contrib.auth.models import AnonymousUser
from Eshopper.models import*
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
import os


dir_path =os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path,'templates/user_wishlist.html')
def my_cron_job():
    user_ = User.objects.all()
   
    wishlist_ = Wishlist.objects.filter(user_id = user_.id)

    html_content = render_to_string(filename,{'wishlist': wishlist_})
    text_content = strip_tags(html_content) 
    
    send_mail(
        'User Wishlist Details',
        text_content,
        settings.EMAIL_HOST_USER ,
        ['admin@neosoft.com'],
        html_message=html_content,
        fail_silently=False)


