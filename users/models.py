from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserOrders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(max_length=64,null=True)
    name=models.CharField(max_length=64)
    size=models.CharField(max_length=64,null=True)
    price=models.DecimalField(max_digits=4,decimal_places=2)
    status=models.CharField(max_length=64,default='initiated')

    def __str__(self):
        return f"{self.name} - ${self.price} "