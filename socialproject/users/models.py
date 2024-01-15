from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/%Y/%m/%d",blank=True)
    
    def __str__(self):
        return self.user.username
    
    
