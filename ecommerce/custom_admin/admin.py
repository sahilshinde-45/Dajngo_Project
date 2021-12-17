from django.contrib import admin
from django.db import models
from .models import BannerHomePage, Cms, Configuration, contactUs,emailTemplate
# Register your models here.

class adminContanctUs(admin.ModelAdmin):
    model = contactUs
    list_display=['name','email','contact_no','note_admin']

admin.site.register(contactUs,adminContanctUs)

class adminEmailTemplate(admin.ModelAdmin):
    model = emailTemplate
    list_display = ['title','content','subject']

admin.site.register(emailTemplate,adminEmailTemplate)


class adminBannerTemplate(admin.ModelAdmin):
    model = BannerHomePage
    list_display = ['name','image']
admin.site.register(BannerHomePage,adminBannerTemplate)

class adminCms(admin.ModelAdmin):
    model = Cms
    list_display = ['title']

admin.site.register(Cms,adminCms)

class adminConfiguration(admin.ModelAdmin):
    model = Configuration
    list_display = ['conf_key']

admin.site.register(Configuration,adminConfiguration)