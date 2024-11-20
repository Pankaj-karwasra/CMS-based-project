from django.contrib import admin
from .models import AddBlog,Profile,Contact,ContactInfo
# Register your models here.,

@admin.register(AddBlog)
class AddAdmin(admin.ModelAdmin):
    list_display = ['id','author','date','title','description','category','image']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','profile_pic','first_name','last_name','skills','bio']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','message']



@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['office_address', 'phone_number', 'email'] 
