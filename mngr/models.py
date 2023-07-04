from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    stock = models.IntegerField(null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

