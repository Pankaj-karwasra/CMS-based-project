from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AddBlog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    date = models.DateField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=70)
    image = models.ImageField(upload_to='uploads/')


# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    profile_pic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    skills = models.CharField(max_length=300)
    bio = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    
# contact 
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.CharField(max_length=1000)


# Contact Info
class ContactInfo(models.Model):
    office_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.office_address
    

