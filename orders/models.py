from django.db import models
from django.contrib.auth.models import User
# Create your models here.

SIZES = (
    ("S", "Small"),
    ("L", "Large")
)

STYLES = (
    ('R', 'Regular'),
    ('S', 'Sicilian')
)

class Pasta(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(help_text="Price in U$S",max_digits=4, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - $ {self.price}"

class Salad(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(help_text="Price in U$S",max_digits=4, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} - $ {self.price}"

class Dinnerplatter(models.Model):
    name = models.CharField(max_length=40)
    small=models.DecimalField(help_text="Price in U$S",max_digits=4, decimal_places=2)
    large=models.DecimalField(help_text="Price in U$S",max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class Sub(models.Model):
    name = models.CharField(max_length=40)
    small=models.DecimalField(help_text="Price in U$S",max_digits=4, decimal_places=2)
    large=models.DecimalField(help_text="Price in U$S",max_digits=4, decimal_places=2)
    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class Topping(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"

class Regular_pizza(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class Sicilian_pizza(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"


class Order2(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(max_length=64,null=True)
    name=models.CharField(max_length=64)
    size=models.CharField(max_length=64,null=True)
    price=models.DecimalField(max_digits=4,decimal_places=2)
    toppings = models.ManyToManyField(Topping)


    def get_cart_total(self,ReqUser):
        sum=0
        for o in Order2.objects.all():
            if o.user == ReqUser:
                sum+=o.price
        return sum

    def __str__(self):
        return f"{self.name} - ${self.price} "

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']



