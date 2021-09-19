from django.db import models
from django.contrib.auth.models import User
from .supporters.actions import save_profile

# Create your models here.

class User_profile(models.Model):
    acc_type_choices=(
        ('Sta','Standard'),
        ('Pro','Professional'),
        ('Dev','Developer'),
        ('Adm','Admin')
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile=models.ImageField(default='profile/544750.jpg',upload_to='profile')
    acc_type=models.CharField(max_length=3,choices=acc_type_choices,default=acc_type_choices[0][0])

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        path=self.profile.path
        save_profile(path)


