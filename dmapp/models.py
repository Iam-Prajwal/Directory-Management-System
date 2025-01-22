from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        
        
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='media/profile_pic')


class directory(models.Model):
    fullname = models.CharField(max_length=200, default="0")
    profession = models.CharField(max_length=200, default="0")
    email = models.CharField(max_length=200, default="0", unique=True)
    mobilenumber = models.CharField(max_length=200, default="0")
    city = models.CharField(max_length=200, default="0")
    address = models.TextField(max_length=200, default="0")
    status = models.CharField(max_length=1, default="0")
    creationdate = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
