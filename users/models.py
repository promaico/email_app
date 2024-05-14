from django.db import models

# Create your models here.

def User(AbstractUser):
    profile_email = models.EmailField(unique=True, null= True)
    
    profile_password = models.CharField(max_length=15, )