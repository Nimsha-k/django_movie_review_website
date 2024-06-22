from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birth_date=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.user.username


